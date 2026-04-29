"""
uxr-bench: basic usage example.

Run without API keys (baseline mode):
    python examples/basic_usage.py

Run with an LLM backend:
    OPENAI_API_KEY=sk-... python examples/basic_usage.py
"""

from uxr_bench.dataset import dataset_stats, get_task, list_tasks
from uxr_bench.evaluator import BenchmarkEvaluator
from uxr_bench.llm import baseline_response


def main():
    # ── 1. Explore the dataset ──────────────────────────────────────────────
    print("=" * 60)
    print("CPR Orbital · uxr-bench · Dataset Overview")
    print("=" * 60)

    stats = dataset_stats()
    print(f"\nTotal tasks : {stats['total']}")
    print("\nBy category:")
    for cat, count in stats["by_category"].items():
        print(f"  {cat:<28} {count}")
    print("\nBy difficulty:")
    for diff, count in stats["by_difficulty"].items():
        print(f"  {diff:<28} {count}")

    # ── 2. Inspect a single task ────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Sample Task: TC-001 (Thematic Coding · Easy)")
    print("=" * 60)

    task = get_task("TC-001")
    print(f"\nDescription : {task.description}")
    print(f"Category    : {task.category.value}")
    print(f"Difficulty  : {task.difficulty.value}")
    print(f"Tags        : {', '.join(task.tags)}")
    print(f"\nGround truth labels:")
    for label in task.ground_truth.labels:
        print(f"  - {label}")

    # ── 3. Baseline evaluation (no API key needed) ──────────────────────────
    print("\n" + "=" * 60)
    print("Baseline Evaluation (keyword heuristic)")
    print("=" * 60)

    evaluator = BenchmarkEvaluator(backend="baseline")
    easy_tasks = list_tasks(difficulty="easy")

    results = evaluator.run_tasks(
        easy_tasks,
        response_fn=baseline_response,
        on_result=lambda r: print(
            f"  {r.task_id}  F1={r.score.f1:.2f}  {'✓' if r.score.passed else '✗'}"
        ),
    )

    report = evaluator.compile_report(results, run_id="basic-usage-demo")

    print(f"\nBaseline Results (easy tasks)")
    print(f"  Pass rate  : {report.pass_rate:.1%}")
    print(f"  Overall F1 : {report.overall_f1:.3f}")

    # ── 4. Per-category summary ─────────────────────────────────────────────
    print("\nBy category:")
    for cat, summary in report.by_category.items():
        print(
            f"  {cat:<28} pass={summary.pass_rate:.0%}  "
            f"F1={summary.mean_f1:.2f}"
        )

    print("\n" + "=" * 60)
    print("To run with an LLM backend:")
    print("  uxr-bench run --all --llm-backend openai")
    print("  uxr-bench run --category bias_detection --llm-backend anthropic")
    print("=" * 60)


if __name__ == "__main__":
    main()
