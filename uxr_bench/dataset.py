"""Dataset loading and filtering for the UXR Benchmark."""
from __future__ import annotations

from ._tasks import BENCHMARK_TASKS
from .models import BenchmarkTask, Difficulty, TaskCategory


def list_tasks(
    category: str | None = None,
    difficulty: str | None = None,
    tag: str | None = None,
) -> list[BenchmarkTask]:
    """Return benchmark tasks, optionally filtered by category, difficulty, or tag."""
    tasks: list[BenchmarkTask] = list(BENCHMARK_TASKS)

    if category:
        tasks = [t for t in tasks if t.category.value == category]
    if difficulty:
        tasks = [t for t in tasks if t.difficulty.value == difficulty]
    if tag:
        tasks = [t for t in tasks if tag in t.tags]

    return tasks


def get_task(task_id: str) -> BenchmarkTask | None:
    """Return a task by ID (case-insensitive), or None if not found."""
    tid = task_id.upper()
    return next((t for t in BENCHMARK_TASKS if t.task_id == tid), None)


def dataset_stats() -> dict:
    """Return summary statistics about the benchmark dataset."""
    tasks = BENCHMARK_TASKS

    by_category: dict[str, int] = {cat.value: 0 for cat in TaskCategory}
    for t in tasks:
        by_category[t.category.value] += 1

    by_difficulty: dict[str, int] = {d.value: 0 for d in Difficulty}
    for t in tasks:
        by_difficulty[t.difficulty.value] += 1

    all_tags: list[str] = []
    for t in tasks:
        all_tags.extend(t.tags)
    unique_tags = sorted(set(all_tags))

    return {
        "total": len(tasks),
        "by_category": by_category,
        "by_difficulty": by_difficulty,
        "unique_tags": unique_tags,
    }


def export_jsonl(tasks: list[BenchmarkTask] | None = None) -> list[dict]:
    """
    Export benchmark tasks as a list of dicts suitable for JSONL serialisation.

    Suitable for fine-tuning data preparation or external evaluation harnesses.
    """
    if tasks is None:
        tasks = list(BENCHMARK_TASKS)

    rows = []
    for t in tasks:
        rows.append(
            {
                "task_id": t.task_id,
                "category": t.category.value,
                "difficulty": t.difficulty.value,
                "description": t.description,
                "input_text": t.input_text,
                "prompt": t.render_prompt(),
                "ground_truth_labels": t.ground_truth.labels,
                "ground_truth_score": t.ground_truth.score,
                "rationale": t.ground_truth.rationale,
                "tags": t.tags,
            }
        )
    return rows
