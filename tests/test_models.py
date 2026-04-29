"""Tests for uxr_bench.models."""
import pytest

from uxr_bench.models import (
    BenchmarkReport,
    BenchmarkTask,
    CategorySummary,
    Difficulty,
    GroundTruth,
    TaskCategory,
    TaskResult,
    TaskScore,
)

# ── TaskCategory ───────────────────────────────────────────────────────────────

def test_task_category_values():
    assert TaskCategory.THEMATIC_CODING.value == "thematic_coding"
    assert TaskCategory.BIAS_DETECTION.value == "bias_detection"
    assert TaskCategory.INSIGHT_EXTRACTION.value == "insight_extraction"
    assert TaskCategory.GUIDE_EVALUATION.value == "guide_evaluation"
    assert TaskCategory.SAY_DO_GAP.value == "say_do_gap"


def test_task_category_count():
    assert len(TaskCategory) == 5


# ── Difficulty ─────────────────────────────────────────────────────────────────

def test_difficulty_values():
    assert Difficulty.EASY.value == "easy"
    assert Difficulty.MEDIUM.value == "medium"
    assert Difficulty.HARD.value == "hard"


def test_difficulty_count():
    assert len(Difficulty) == 3


# ── GroundTruth ────────────────────────────────────────────────────────────────

def test_ground_truth_labels_only():
    gt = GroundTruth(labels=["theme_a", "theme_b"])
    assert gt.labels == ["theme_a", "theme_b"]
    assert gt.score is None
    assert gt.rationale == ""


def test_ground_truth_with_score():
    gt = GroundTruth(labels=["neutral"], score=75.0, rationale="Good guide")
    assert gt.score == 75.0
    assert gt.rationale == "Good guide"


# ── BenchmarkTask ──────────────────────────────────────────────────────────────

def _make_task(**kwargs) -> BenchmarkTask:
    defaults = dict(
        task_id="TC-TEST",
        category=TaskCategory.THEMATIC_CODING,
        difficulty=Difficulty.EASY,
        description="Test task",
        input_text="Some text about privacy and trust.",
        prompt_template="Identify themes:\n{input_text}\n\nThemes:",
        ground_truth=GroundTruth(labels=["privacy", "trust"]),
    )
    defaults.update(kwargs)
    return BenchmarkTask(**defaults)


def test_benchmark_task_creation():
    task = _make_task()
    assert task.task_id == "TC-TEST"
    assert task.category == TaskCategory.THEMATIC_CODING
    assert task.difficulty == Difficulty.EASY


def test_render_prompt_interpolates_input():
    task = _make_task()
    rendered = task.render_prompt()
    assert "Some text about privacy and trust." in rendered
    assert "{input_text}" not in rendered


def test_benchmark_task_default_tags():
    task = _make_task()
    assert task.tags == []


def test_benchmark_task_with_tags():
    task = _make_task(tags=["privacy", "trust"])
    assert "privacy" in task.tags


# ── TaskScore ──────────────────────────────────────────────────────────────────

def test_task_score_defaults():
    score = TaskScore()
    assert score.precision == 0.0
    assert score.recall == 0.0
    assert score.f1 == 0.0
    assert score.passed is False
    assert score.numeric_score is None


def test_task_score_custom():
    score = TaskScore(precision=0.8, recall=0.6, f1=0.686, passed=True)
    assert score.passed is True
    assert score.f1 == pytest.approx(0.686)


# ── TaskResult ─────────────────────────────────────────────────────────────────

def test_task_result_creation():
    score = TaskScore(f1=0.75, passed=True)
    result = TaskResult(
        task_id="TC-001",
        category=TaskCategory.THEMATIC_CODING,
        difficulty=Difficulty.EASY,
        raw_response="privacy, trust",
        predicted_labels=["privacy", "trust"],
        score=score,
        backend="openai",
    )
    assert result.task_id == "TC-001"
    assert result.backend == "openai"
    assert result.score.passed is True


def test_task_result_default_backend():
    score = TaskScore()
    result = TaskResult(
        task_id="TC-001",
        category=TaskCategory.THEMATIC_CODING,
        difficulty=Difficulty.EASY,
        raw_response="",
        predicted_labels=[],
        score=score,
    )
    assert result.backend == "baseline"


# ── CategorySummary ────────────────────────────────────────────────────────────

def test_category_summary_creation():
    s = CategorySummary(
        category="thematic_coding",
        tasks_run=5,
        tasks_passed=3,
        mean_f1=0.62,
        pass_rate=0.6,
    )
    assert s.tasks_run == 5
    assert s.pass_rate == 0.6


# ── BenchmarkReport ────────────────────────────────────────────────────────────

def _make_report(**kwargs) -> BenchmarkReport:
    defaults = dict(
        run_id="abc12345",
        timestamp="2026-05-01T00:00:00+00:00",
        backend="baseline",
        tasks_total=5,
        tasks_passed=3,
        overall_f1=0.55,
        by_category={},
        by_difficulty={},
        results=[],
    )
    defaults.update(kwargs)
    return BenchmarkReport(**defaults)


def test_benchmark_report_pass_rate():
    report = _make_report(tasks_total=10, tasks_passed=7)
    assert report.pass_rate == pytest.approx(0.7)


def test_benchmark_report_pass_rate_zero_total():
    report = _make_report(tasks_total=0, tasks_passed=0)
    assert report.pass_rate == 0.0


def test_benchmark_report_fields():
    report = _make_report()
    assert report.run_id == "abc12345"
    assert report.backend == "baseline"
    assert report.overall_f1 == 0.55
