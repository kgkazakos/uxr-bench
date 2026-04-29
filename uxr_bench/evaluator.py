"""Benchmark evaluation engine — scores LLM (or baseline) responses against ground truth."""
from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import datetime, timezone

from .metrics import (
    extract_numeric_score,
    normalise_label,
    parse_labels,
    partial_match_f1,
    precision_recall_f1,
    score_numeric_proximity,
)
from .models import (
    BenchmarkReport,
    BenchmarkTask,
    CategorySummary,
    Difficulty,
    TaskCategory,
    TaskResult,
    TaskScore,
)

# Minimum F1 (or proximity score) to be counted as a passing result
PASS_THRESHOLD = 0.5

# Guide evaluation: within this many points = pass
GUIDE_PASS_TOLERANCE = 20.0

ResponseFn = Callable[[BenchmarkTask], str]


class BenchmarkEvaluator:
    """Orchestrates benchmark runs and compiles summary reports."""

    def __init__(self, backend: str = "baseline") -> None:
        self.backend = backend

    # ------------------------------------------------------------------ #
    # Scoring                                                               #
    # ------------------------------------------------------------------ #

    def score_task(self, task: BenchmarkTask, raw_response: str) -> TaskResult:
        """Score a single raw LLM (or baseline) response against the task's ground truth."""
        if task.category == TaskCategory.GUIDE_EVALUATION:
            return self._score_guide_eval(task, raw_response)
        return self._score_label_task(task, raw_response)

    def _score_label_task(self, task: BenchmarkTask, raw_response: str) -> TaskResult:
        """Score tasks that expect a list of labels (thematic coding, bias, insight, say-do)."""
        predicted = parse_labels(raw_response)
        gt = [normalise_label(lbl) for lbl in task.ground_truth.labels]

        # Insight extraction uses partial token-overlap matching; all others use exact set match
        if task.category == TaskCategory.INSIGHT_EXTRACTION:
            precision, recall, f1 = partial_match_f1(predicted, gt, threshold=0.4)
        else:
            precision, recall, f1 = precision_recall_f1(predicted, gt)

        passed = f1 >= PASS_THRESHOLD
        pred_set = set(predicted)
        gt_set = set(gt)

        score = TaskScore(
            precision=round(precision, 4),
            recall=round(recall, 4),
            f1=round(f1, 4),
            passed=passed,
            details={
                "predicted": predicted,
                "ground_truth": gt,
                "true_positives": sorted(pred_set & gt_set),
                "false_positives": sorted(pred_set - gt_set),
                "false_negatives": sorted(gt_set - pred_set),
            },
        )
        return TaskResult(
            task_id=task.task_id,
            category=task.category,
            difficulty=task.difficulty,
            raw_response=raw_response,
            predicted_labels=predicted,
            score=score,
            backend=self.backend,
        )

    def _score_guide_eval(self, task: BenchmarkTask, raw_response: str) -> TaskResult:
        """Score guide evaluation tasks by numeric proximity to the ground-truth score."""
        predicted_score = extract_numeric_score(raw_response)
        gt_score = task.ground_truth.score if task.ground_truth.score is not None else 50.0

        if predicted_score is None:
            proximity = 0.0
            passed = False
            diff = None
        else:
            proximity = score_numeric_proximity(predicted_score, gt_score)
            diff = abs(predicted_score - gt_score)
            passed = diff <= GUIDE_PASS_TOLERANCE

        score = TaskScore(
            precision=round(proximity, 4),
            recall=round(proximity, 4),
            f1=round(proximity, 4),
            numeric_score=predicted_score,
            passed=passed,
            details={
                "predicted_score": predicted_score,
                "ground_truth_score": gt_score,
                "difference": round(diff, 1) if diff is not None else None,
            },
        )
        predicted_labels = [str(predicted_score)] if predicted_score is not None else []
        return TaskResult(
            task_id=task.task_id,
            category=task.category,
            difficulty=task.difficulty,
            raw_response=raw_response,
            predicted_labels=predicted_labels,
            score=score,
            backend=self.backend,
        )

    # ------------------------------------------------------------------ #
    # Execution                                                             #
    # ------------------------------------------------------------------ #

    def run_task(self, task: BenchmarkTask, response_fn: ResponseFn) -> TaskResult:
        """Call ``response_fn(task)`` to get a raw response, then score it."""
        raw = response_fn(task)
        return self.score_task(task, raw)

    def run_tasks(
        self,
        tasks: list[BenchmarkTask],
        response_fn: ResponseFn,
        on_result: Callable[[TaskResult], None] | None = None,
    ) -> list[TaskResult]:
        """Run multiple tasks and optionally call ``on_result`` after each."""
        results = []
        for task in tasks:
            result = self.run_task(task, response_fn)
            if on_result:
                on_result(result)
            results.append(result)
        return results

    # ------------------------------------------------------------------ #
    # Reporting                                                             #
    # ------------------------------------------------------------------ #

    def compile_report(
        self,
        results: list[TaskResult],
        run_id: str | None = None,
    ) -> BenchmarkReport:
        """Compile a :class:`BenchmarkReport` from a list of :class:`TaskResult` objects."""
        if not run_id:
            run_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now(timezone.utc).isoformat()

        tasks_total = len(results)
        tasks_passed = sum(1 for r in results if r.score.passed)
        overall_f1 = (
            sum(r.score.f1 for r in results) / tasks_total if tasks_total else 0.0
        )

        # Aggregate by category
        by_category: dict[str, CategorySummary] = {}
        for cat in TaskCategory:
            cat_results = [r for r in results if r.category == cat]
            if not cat_results:
                continue
            passed = sum(1 for r in cat_results if r.score.passed)
            mean_f1 = sum(r.score.f1 for r in cat_results) / len(cat_results)
            by_category[cat.value] = CategorySummary(
                category=cat.value,
                tasks_run=len(cat_results),
                tasks_passed=passed,
                mean_f1=round(mean_f1, 4),
                pass_rate=round(passed / len(cat_results), 4),
            )

        # Aggregate by difficulty
        by_difficulty: dict[str, dict] = {}
        for diff in Difficulty:
            d_results = [r for r in results if r.difficulty == diff]
            if not d_results:
                continue
            d_passed = sum(1 for r in d_results if r.score.passed)
            by_difficulty[diff.value] = {
                "tasks_run": len(d_results),
                "tasks_passed": d_passed,
                "mean_f1": round(sum(r.score.f1 for r in d_results) / len(d_results), 4),
            }

        return BenchmarkReport(
            run_id=run_id,
            timestamp=timestamp,
            backend=self.backend,
            tasks_total=tasks_total,
            tasks_passed=tasks_passed,
            overall_f1=round(overall_f1, 4),
            by_category=by_category,
            by_difficulty=by_difficulty,
            results=results,
        )
