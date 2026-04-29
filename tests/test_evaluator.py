"""Tests for uxr_bench.evaluator."""
import pytest

from uxr_bench.evaluator import GUIDE_PASS_TOLERANCE, PASS_THRESHOLD, BenchmarkEvaluator
from uxr_bench.models import (
    BenchmarkTask,
    Difficulty,
    GroundTruth,
    TaskCategory,
    TaskResult,
    TaskScore,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_label_task(
    task_id="TC-TEST",
    category=TaskCategory.THEMATIC_CODING,
    difficulty=Difficulty.EASY,
    gt_labels=None,
) -> BenchmarkTask:
    return BenchmarkTask(
        task_id=task_id,
        category=category,
        difficulty=difficulty,
        description="Test task",
        input_text="Participant discusses privacy and trust in the app.",
        prompt_template="Themes:\n{input_text}\n\nThemes:",
        ground_truth=GroundTruth(labels=gt_labels or ["privacy", "trust"]),
    )


def _make_guide_task(gt_score=75.0) -> BenchmarkTask:
    return BenchmarkTask(
        task_id="GE-TEST",
        category=TaskCategory.GUIDE_EVALUATION,
        difficulty=Difficulty.MEDIUM,
        description="Test guide task",
        input_text="1. Tell me about privacy. 2. Tell me about trust.",
        prompt_template="Score:\n{input_text}\n\nScore:",
        ground_truth=GroundTruth(labels=["neutrality"], score=gt_score),
    )


# ── BenchmarkEvaluator init ────────────────────────────────────────────────────

def test_evaluator_default_backend():
    ev = BenchmarkEvaluator()
    assert ev.backend == "baseline"


def test_evaluator_custom_backend():
    ev = BenchmarkEvaluator(backend="openai")
    assert ev.backend == "openai"


# ── score_task: label tasks ────────────────────────────────────────────────────

def test_score_task_perfect_match():
    ev = BenchmarkEvaluator()
    task = _make_label_task(gt_labels=["privacy", "trust"])
    result = ev.score_task(task, "privacy, trust")
    assert result.score.f1 == pytest.approx(1.0)
    assert result.score.passed is True


def test_score_task_no_match():
    ev = BenchmarkEvaluator()
    task = _make_label_task(gt_labels=["privacy", "trust"])
    result = ev.score_task(task, "onboarding, friction")
    assert result.score.f1 == 0.0
    assert result.score.passed is False


def test_score_task_partial_match():
    ev = BenchmarkEvaluator()
    task = _make_label_task(gt_labels=["privacy", "trust", "control"])
    result = ev.score_task(task, "privacy, trust")
    assert 0 < result.score.f1 < 1.0


def test_score_task_empty_response():
    ev = BenchmarkEvaluator()
    task = _make_label_task(gt_labels=["privacy"])
    result = ev.score_task(task, "")
    assert result.score.f1 == 0.0
    assert result.score.passed is False


def test_score_task_details_have_tp_fp_fn():
    ev = BenchmarkEvaluator()
    task = _make_label_task(gt_labels=["privacy", "trust"])
    result = ev.score_task(task, "privacy, control")
    assert "true_positives" in result.score.details
    assert "false_positives" in result.score.details
    assert "false_negatives" in result.score.details
    assert "privacy" in result.score.details["true_positives"]
    assert "control" in result.score.details["false_positives"]
    assert "trust" in result.score.details["false_negatives"]


def test_score_task_bias_category():
    ev = BenchmarkEvaluator()
    task = _make_label_task(
        category=TaskCategory.BIAS_DETECTION,
        gt_labels=["leading_question", "anchoring_bias"],
    )
    result = ev.score_task(task, "leading_question, anchoring_bias")
    assert result.score.f1 == pytest.approx(1.0)


def test_score_task_say_do_category():
    ev = BenchmarkEvaluator()
    task = _make_label_task(
        category=TaskCategory.SAY_DO_GAP,
        gt_labels=["privacy_paradox", "attitude_behavior_inconsistency"],
    )
    result = ev.score_task(task, "privacy_paradox, attitude_behavior_inconsistency")
    assert result.score.passed is True


# ── score_task: insight_extraction (partial match) ────────────────────────────

def test_score_task_insight_uses_partial_match():
    ev = BenchmarkEvaluator()
    task = _make_label_task(
        category=TaskCategory.INSIGHT_EXTRACTION,
        gt_labels=["privacy_concern", "design_opportunity"],
    )
    # "privacy_paradox" shares "privacy" token — should get partial credit
    result = ev.score_task(task, "privacy_paradox, design_opportunity")
    # Should score higher than exact F1 would suggest
    assert result.score.f1 > 0


def test_score_task_insight_no_overlap():
    ev = BenchmarkEvaluator()
    task = _make_label_task(
        category=TaskCategory.INSIGHT_EXTRACTION,
        gt_labels=["privacy_concern", "design_opportunity"],
    )
    result = ev.score_task(task, "alpha_beta, gamma_delta")
    assert result.score.f1 == 0.0


# ── score_task: guide_evaluation ──────────────────────────────────────────────

def test_score_guide_exact_score():
    ev = BenchmarkEvaluator()
    task = _make_guide_task(gt_score=75.0)
    result = ev.score_task(task, "75")
    assert result.score.f1 == pytest.approx(1.0)
    assert result.score.passed is True
    assert result.score.numeric_score == 75.0


def test_score_guide_within_tolerance_passes():
    ev = BenchmarkEvaluator()
    task = _make_guide_task(gt_score=75.0)
    result = ev.score_task(task, "85")  # 10 points off
    assert result.score.passed is True


def test_score_guide_outside_tolerance_fails():
    ev = BenchmarkEvaluator()
    task = _make_guide_task(gt_score=75.0)
    result = ev.score_task(task, "45")  # 30 points off
    assert result.score.passed is False


def test_score_guide_no_numeric_fails():
    ev = BenchmarkEvaluator()
    task = _make_guide_task(gt_score=75.0)
    result = ev.score_task(task, "the guide is good quality")
    assert result.score.passed is False
    assert result.score.numeric_score is None


def test_score_guide_score_from_prose():
    ev = BenchmarkEvaluator()
    task = _make_guide_task(gt_score=82.0)
    result = ev.score_task(task, "I would score this guide 78 out of 100.")
    assert result.score.numeric_score == pytest.approx(78.0)


# ── run_task ───────────────────────────────────────────────────────────────────

def test_run_task_calls_response_fn():
    ev = BenchmarkEvaluator()
    task = _make_label_task(gt_labels=["privacy", "trust"])
    calls = []

    def fn(t):
        calls.append(t.task_id)
        return "privacy, trust"

    result = ev.run_task(task, fn)
    assert calls == ["TC-TEST"]
    assert result.score.f1 == pytest.approx(1.0)


def test_run_task_returns_task_result():
    ev = BenchmarkEvaluator()
    task = _make_label_task()
    result = ev.run_task(task, lambda t: "privacy")
    assert isinstance(result, TaskResult)


# ── run_tasks ──────────────────────────────────────────────────────────────────

def test_run_tasks_multiple():
    ev = BenchmarkEvaluator()
    tasks = [
        _make_label_task(task_id=f"T-{i}", gt_labels=["privacy"])
        for i in range(3)
    ]
    results = ev.run_tasks(tasks, lambda t: "privacy")
    assert len(results) == 3
    assert all(r.score.passed for r in results)


def test_run_tasks_on_result_callback():
    ev = BenchmarkEvaluator()
    tasks = [_make_label_task(task_id=f"T-{i}") for i in range(2)]
    seen = []
    ev.run_tasks(tasks, lambda t: "privacy", on_result=lambda r: seen.append(r.task_id))
    assert len(seen) == 2


# ── compile_report ─────────────────────────────────────────────────────────────

def _make_result(task_id, cat, diff, passed, f1=None) -> TaskResult:
    f1_val = f1 if f1 is not None else (0.8 if passed else 0.2)
    score = TaskScore(f1=f1_val, passed=passed)
    return TaskResult(
        task_id=task_id,
        category=cat,
        difficulty=diff,
        raw_response="",
        predicted_labels=[],
        score=score,
    )


def test_compile_report_basic():
    ev = BenchmarkEvaluator()
    results = [
        _make_result("TC-001", TaskCategory.THEMATIC_CODING, Difficulty.EASY, True),
        _make_result("TC-002", TaskCategory.THEMATIC_CODING, Difficulty.MEDIUM, False),
    ]
    report = ev.compile_report(results)
    assert report.tasks_total == 2
    assert report.tasks_passed == 1


def test_compile_report_pass_rate():
    ev = BenchmarkEvaluator()
    results = [
        _make_result(f"T-{i}", TaskCategory.THEMATIC_CODING, Difficulty.EASY, i < 7)
        for i in range(10)
    ]
    report = ev.compile_report(results)
    assert report.pass_rate == pytest.approx(0.7)


def test_compile_report_by_category():
    ev = BenchmarkEvaluator()
    results = [
        _make_result("TC-001", TaskCategory.THEMATIC_CODING, Difficulty.EASY, True),
        _make_result("BD-001", TaskCategory.BIAS_DETECTION, Difficulty.EASY, False),
    ]
    report = ev.compile_report(results)
    assert "thematic_coding" in report.by_category
    assert "bias_detection" in report.by_category
    assert report.by_category["thematic_coding"].tasks_passed == 1
    assert report.by_category["bias_detection"].tasks_passed == 0


def test_compile_report_by_difficulty():
    ev = BenchmarkEvaluator()
    results = [
        _make_result("TC-001", TaskCategory.THEMATIC_CODING, Difficulty.EASY, True),
        _make_result("TC-002", TaskCategory.THEMATIC_CODING, Difficulty.HARD, False),
    ]
    report = ev.compile_report(results)
    assert "easy" in report.by_difficulty
    assert "hard" in report.by_difficulty


def test_compile_report_overall_f1():
    ev = BenchmarkEvaluator()
    results = [
        _make_result("T-1", TaskCategory.THEMATIC_CODING, Difficulty.EASY, True, f1=0.8),
        _make_result("T-2", TaskCategory.THEMATIC_CODING, Difficulty.EASY, True, f1=0.6),
    ]
    report = ev.compile_report(results)
    assert report.overall_f1 == pytest.approx(0.7)


def test_compile_report_generates_run_id():
    ev = BenchmarkEvaluator()
    report = ev.compile_report([])
    assert len(report.run_id) > 0


def test_compile_report_custom_run_id():
    ev = BenchmarkEvaluator()
    report = ev.compile_report([], run_id="my-run-01")
    assert report.run_id == "my-run-01"


def test_compile_report_has_timestamp():
    ev = BenchmarkEvaluator()
    report = ev.compile_report([])
    assert "2026" in report.timestamp or "202" in report.timestamp


def test_compile_report_empty_results():
    ev = BenchmarkEvaluator()
    report = ev.compile_report([])
    assert report.tasks_total == 0
    assert report.pass_rate == 0.0
    assert report.overall_f1 == 0.0


# ── pass threshold ─────────────────────────────────────────────────────────────

def test_pass_threshold_value():
    assert PASS_THRESHOLD == 0.5


def test_guide_pass_tolerance_value():
    assert GUIDE_PASS_TOLERANCE == 20.0
