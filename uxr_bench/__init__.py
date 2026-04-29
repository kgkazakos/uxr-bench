"""UXR-Bench: Benchmark dataset for evaluating LLM performance on qualitative UX research tasks."""
from .dataset import dataset_stats, export_jsonl, get_task, list_tasks
from .evaluator import BenchmarkEvaluator
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
    GroundTruth,
    TaskCategory,
    TaskResult,
    TaskScore,
)

__version__ = "0.1.0"
__all__ = [
    "BenchmarkEvaluator",
    "BenchmarkReport",
    "BenchmarkTask",
    "CategorySummary",
    "Difficulty",
    "GroundTruth",
    "TaskCategory",
    "TaskResult",
    "TaskScore",
    "dataset_stats",
    "export_jsonl",
    "get_task",
    "list_tasks",
    "extract_numeric_score",
    "normalise_label",
    "parse_labels",
    "partial_match_f1",
    "precision_recall_f1",
    "score_numeric_proximity",
]
