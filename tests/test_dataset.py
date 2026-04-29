"""Tests for uxr_bench.dataset."""
import pytest

from uxr_bench.dataset import dataset_stats, export_jsonl, get_task, list_tasks
from uxr_bench.models import Difficulty, TaskCategory

# ── list_tasks ─────────────────────────────────────────────────────────────────

def test_list_tasks_all():
    tasks = list_tasks()
    assert len(tasks) == 25


def test_list_tasks_category_thematic():
    tasks = list_tasks(category="thematic_coding")
    assert len(tasks) == 5
    assert all(t.category == TaskCategory.THEMATIC_CODING for t in tasks)


def test_list_tasks_category_bias():
    tasks = list_tasks(category="bias_detection")
    assert len(tasks) == 5
    assert all(t.category == TaskCategory.BIAS_DETECTION for t in tasks)


def test_list_tasks_category_insight():
    tasks = list_tasks(category="insight_extraction")
    assert len(tasks) == 5


def test_list_tasks_category_guide():
    tasks = list_tasks(category="guide_evaluation")
    assert len(tasks) == 5


def test_list_tasks_category_say_do():
    tasks = list_tasks(category="say_do_gap")
    assert len(tasks) == 5


def test_list_tasks_difficulty_easy():
    tasks = list_tasks(difficulty="easy")
    assert all(t.difficulty == Difficulty.EASY for t in tasks)
    assert len(tasks) > 0


def test_list_tasks_difficulty_medium():
    tasks = list_tasks(difficulty="medium")
    assert all(t.difficulty == Difficulty.MEDIUM for t in tasks)


def test_list_tasks_difficulty_hard():
    tasks = list_tasks(difficulty="hard")
    assert all(t.difficulty == Difficulty.HARD for t in tasks)


def test_list_tasks_combined_filter():
    tasks = list_tasks(category="thematic_coding", difficulty="easy")
    assert len(tasks) == 1
    assert tasks[0].task_id == "TC-001"


def test_list_tasks_tag_filter():
    tasks = list_tasks(tag="fintech")
    assert len(tasks) > 0
    assert all("fintech" in t.tags for t in tasks)


def test_list_tasks_unknown_tag_returns_empty():
    tasks = list_tasks(tag="nonexistent_tag_xyz")
    assert tasks == []


# ── get_task ───────────────────────────────────────────────────────────────────

def test_get_task_found():
    task = get_task("TC-001")
    assert task is not None
    assert task.task_id == "TC-001"


def test_get_task_case_insensitive():
    task = get_task("tc-001")
    assert task is not None
    assert task.task_id == "TC-001"


def test_get_task_not_found():
    assert get_task("XX-999") is None


def test_get_task_guide():
    task = get_task("GE-002")
    assert task is not None
    assert task.ground_truth.score == pytest.approx(28.0)


def test_get_task_say_do():
    task = get_task("SD-005")
    assert task is not None
    assert "self_serving_rationalization" in task.ground_truth.labels


# ── dataset_stats ──────────────────────────────────────────────────────────────

def test_dataset_stats_total():
    stats = dataset_stats()
    assert stats["total"] == 25


def test_dataset_stats_by_category_keys():
    stats = dataset_stats()
    for cat in TaskCategory:
        assert cat.value in stats["by_category"]


def test_dataset_stats_category_counts():
    stats = dataset_stats()
    for cat in TaskCategory:
        assert stats["by_category"][cat.value] == 5


def test_dataset_stats_difficulty_totals():
    stats = dataset_stats()
    total = sum(stats["by_difficulty"].values())
    assert total == 25


def test_dataset_stats_has_unique_tags():
    stats = dataset_stats()
    assert "unique_tags" in stats
    assert len(stats["unique_tags"]) > 0


# ── export_jsonl ───────────────────────────────────────────────────────────────

def test_export_jsonl_all():
    rows = export_jsonl()
    assert len(rows) == 25


def test_export_jsonl_required_keys():
    rows = export_jsonl()
    required = {
        "task_id", "category", "difficulty", "description",
        "input_text", "prompt", "ground_truth_labels",
        "ground_truth_score", "rationale", "tags",
    }
    for row in rows:
        assert required.issubset(row.keys())


def test_export_jsonl_prompt_rendered():
    rows = export_jsonl()
    for row in rows:
        assert "{input_text}" not in row["prompt"]
        assert row["input_text"] in row["prompt"]


def test_export_jsonl_category_filter():
    tasks = list_tasks(category="bias_detection")
    rows = export_jsonl(tasks)
    assert len(rows) == 5
    assert all(r["category"] == "bias_detection" for r in rows)


def test_export_jsonl_guide_has_score():
    tasks = list_tasks(category="guide_evaluation")
    rows = export_jsonl(tasks)
    assert all(r["ground_truth_score"] is not None for r in rows)


def test_export_jsonl_non_guide_score_is_none():
    tasks = list_tasks(category="thematic_coding")
    rows = export_jsonl(tasks)
    assert all(r["ground_truth_score"] is None for r in rows)


# ── task integrity ─────────────────────────────────────────────────────────────

def test_task_ids_are_unique():
    tasks = list_tasks()
    ids = [t.task_id for t in tasks]
    assert len(ids) == len(set(ids))


def test_all_tasks_have_labels():
    tasks = list_tasks()
    for t in tasks:
        assert len(t.ground_truth.labels) > 0, f"{t.task_id} has no ground truth labels"


def test_guide_tasks_have_numeric_score():
    tasks = list_tasks(category="guide_evaluation")
    for t in tasks:
        assert t.ground_truth.score is not None, f"{t.task_id} missing numeric score"
        assert 0 <= t.ground_truth.score <= 100
