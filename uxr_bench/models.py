"""Data models for the UXR Benchmark."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskCategory(str, Enum):
    THEMATIC_CODING = "thematic_coding"
    BIAS_DETECTION = "bias_detection"
    INSIGHT_EXTRACTION = "insight_extraction"
    GUIDE_EVALUATION = "guide_evaluation"
    SAY_DO_GAP = "say_do_gap"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass
class GroundTruth:
    """Ground truth annotations for a benchmark task."""

    labels: list[str]
    score: float | None = None  # numeric GT for guide_evaluation
    rationale: str = ""


@dataclass
class BenchmarkTask:
    """A single benchmark task with input, prompt, and ground truth."""

    task_id: str
    category: TaskCategory
    difficulty: Difficulty
    description: str
    input_text: str
    prompt_template: str
    ground_truth: GroundTruth
    tags: list[str] = field(default_factory=list)

    def render_prompt(self) -> str:
        """Render the prompt template with the task's input text."""
        return self.prompt_template.format(input_text=self.input_text)


@dataclass
class TaskScore:
    """Scoring breakdown for a single task result."""

    precision: float = 0.0
    recall: float = 0.0
    f1: float = 0.0
    numeric_score: float | None = None  # predicted score for guide_evaluation
    passed: bool = False
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskResult:
    """The output of running a single benchmark task."""

    task_id: str
    category: TaskCategory
    difficulty: Difficulty
    raw_response: str
    predicted_labels: list[str]
    score: TaskScore
    backend: str = "baseline"


@dataclass
class CategorySummary:
    """Aggregated metrics for one task category."""

    category: str
    tasks_run: int
    tasks_passed: int
    mean_f1: float
    pass_rate: float


@dataclass
class BenchmarkReport:
    """Full benchmark run report."""

    run_id: str
    timestamp: str
    backend: str
    tasks_total: int
    tasks_passed: int
    overall_f1: float
    by_category: dict[str, CategorySummary]
    by_difficulty: dict[str, dict[str, Any]]
    results: list[TaskResult]

    @property
    def pass_rate(self) -> float:
        if self.tasks_total == 0:
            return 0.0
        return self.tasks_passed / self.tasks_total
