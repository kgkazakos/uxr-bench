"""Click CLI for uxr-bench."""
from __future__ import annotations

import json
import sys

import click
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .dataset import dataset_stats, export_jsonl, get_task, list_tasks
from .evaluator import BenchmarkEvaluator
from .models import Difficulty, TaskCategory

console = Console()

CATEGORIES = [c.value for c in TaskCategory]
DIFFICULTIES = [d.value for d in Difficulty]


# ──────────────────────────────────────────────────────────────────────────────
# CLI Group
# ──────────────────────────────────────────────────────────────────────────────


@click.group()
@click.version_option(version="0.1.0", prog_name="uxr-bench")
def cli() -> None:
    """UXR-Bench: benchmark LLM performance on qualitative UX research tasks."""


# ──────────────────────────────────────────────────────────────────────────────
# list
# ──────────────────────────────────────────────────────────────────────────────


@cli.command("list")
@click.option("--category", "-c", type=click.Choice(CATEGORIES), help="Filter by category")
@click.option("--difficulty", "-d", type=click.Choice(DIFFICULTIES), help="Filter by difficulty")
@click.option("--tag", "-t", help="Filter by tag")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def list_cmd(category: str, difficulty: str, tag: str, as_json: bool) -> None:
    """List benchmark tasks with optional filters."""
    tasks = list_tasks(category=category, difficulty=difficulty, tag=tag)

    if as_json:
        click.echo(
            json.dumps(
                [
                    {
                        "task_id": t.task_id,
                        "category": t.category.value,
                        "difficulty": t.difficulty.value,
                        "description": t.description,
                        "tags": t.tags,
                    }
                    for t in tasks
                ],
                indent=2,
            )
        )
        return

    diff_colour = {"easy": "green", "medium": "yellow", "hard": "red"}
    table = Table(box=box.SIMPLE_HEAD, show_lines=False)
    table.add_column("ID", style="bold cyan", no_wrap=True, width=8)
    table.add_column("Category", width=22)
    table.add_column("Diff", width=8)
    table.add_column("Description")

    for t in tasks:
        c = diff_colour.get(t.difficulty.value, "white")
        table.add_row(
            t.task_id,
            t.category.value.replace("_", " "),
            f"[{c}]{t.difficulty.value}[/{c}]",
            t.description,
        )

    console.print(table)
    console.print(f"[dim]{len(tasks)} task(s)[/dim]")


# ──────────────────────────────────────────────────────────────────────────────
# show
# ──────────────────────────────────────────────────────────────────────────────


@cli.command("show")
@click.argument("task_id")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def show_cmd(task_id: str, as_json: bool) -> None:
    """Show full details of a benchmark task."""
    task = get_task(task_id)
    if task is None:
        console.print(f"[red]Task '{task_id}' not found.[/red]")
        sys.exit(1)

    if as_json:
        click.echo(
            json.dumps(
                {
                    "task_id": task.task_id,
                    "category": task.category.value,
                    "difficulty": task.difficulty.value,
                    "description": task.description,
                    "input_text": task.input_text,
                    "prompt": task.render_prompt(),
                    "ground_truth_labels": task.ground_truth.labels,
                    "ground_truth_score": task.ground_truth.score,
                    "rationale": task.ground_truth.rationale,
                    "tags": task.tags,
                },
                indent=2,
            )
        )
        return

    console.print(
        Panel(
            f"[bold]{task.task_id}[/bold]  ·  "
            f"{task.category.value.replace('_', ' ')}  ·  {task.difficulty.value}\n"
            f"[dim]{task.description}[/dim]",
            title="Task",
            border_style="cyan",
        )
    )
    console.print("\n[bold]Input text:[/bold]")
    console.print(task.input_text)
    console.print("\n[bold]Ground truth labels:[/bold]")
    console.print(", ".join(task.ground_truth.labels))
    if task.ground_truth.score is not None:
        console.print(f"\n[bold]Ground truth score:[/bold] {task.ground_truth.score}")
    console.print(f"\n[bold]Rationale:[/bold] [dim]{task.ground_truth.rationale}[/dim]")
    if task.tags:
        console.print(f"\n[bold]Tags:[/bold] {', '.join(task.tags)}")


# ──────────────────────────────────────────────────────────────────────────────
# run
# ──────────────────────────────────────────────────────────────────────────────


@cli.command("run")
@click.option("--task", "-t", "task_id", help="Run a specific task by ID")
@click.option(
    "--category",
    "-c",
    type=click.Choice(CATEGORIES),
    help="Run all tasks in a category",
)
@click.option(
    "--difficulty",
    "-d",
    type=click.Choice(DIFFICULTIES),
    help="Filter by difficulty (combine with --category or --all)",
)
@click.option("--all", "run_all", is_flag=True, help="Run the full benchmark")
@click.option(
    "--llm-backend",
    type=click.Choice(["openai", "anthropic", "gemini"]),
    help="LLM backend (default: keyword baseline)",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def run_cmd(
    task_id: str,
    category: str,
    difficulty: str,
    run_all: bool,
    llm_backend: str,
    as_json: bool,
) -> None:
    """Run benchmark tasks and score the results."""
    # Resolve task list
    if task_id:
        task = get_task(task_id)
        if task is None:
            console.print(f"[red]Task '{task_id}' not found.[/red]")
            sys.exit(1)
        tasks = [task]
    elif run_all:
        tasks = list_tasks(difficulty=difficulty)
    elif category:
        tasks = list_tasks(category=category, difficulty=difficulty)
    else:
        console.print("[yellow]Specify --task TASK_ID, --category CATEGORY, or --all.[/yellow]")
        sys.exit(1)

    backend_name = llm_backend or "baseline"
    evaluator = BenchmarkEvaluator(backend=backend_name)

    if llm_backend:
        try:
            from .llm import make_llm_response_fn

            response_fn = make_llm_response_fn(llm_backend)
        except ImportError as exc:
            console.print(f"[red]{exc}[/red]")
            sys.exit(1)
    else:
        response_fn = _baseline_response_fn

    results = []
    status_msg = f"[cyan]Running {len(tasks)} task(s) [{backend_name}]…[/cyan]"
    with console.status(status_msg):
        for task in tasks:
            result = evaluator.run_task(task, response_fn)
            results.append(result)

    report = evaluator.compile_report(results)

    if as_json:
        click.echo(_report_to_json(report))
        return

    _print_report(report)


# ──────────────────────────────────────────────────────────────────────────────
# stats
# ──────────────────────────────────────────────────────────────────────────────


@cli.command("stats")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def stats_cmd(as_json: bool) -> None:
    """Show dataset statistics."""
    stats = dataset_stats()

    if as_json:
        click.echo(json.dumps(stats, indent=2))
        return

    cat_lines = "\n".join(f"  {k.replace('_',' ')}: {v}" for k, v in stats["by_category"].items())
    diff_lines = "\n".join(f"  {k}: {v}" for k, v in stats["by_difficulty"].items())
    console.print(
        Panel(
            f"[bold]Total tasks:[/bold] {stats['total']}\n\n"
            f"[bold]By category:[/bold]\n{cat_lines}\n\n"
            f"[bold]By difficulty:[/bold]\n{diff_lines}",
            title="UXR-Bench Dataset",
            border_style="green",
        )
    )


# ──────────────────────────────────────────────────────────────────────────────
# export
# ──────────────────────────────────────────────────────────────────────────────


@cli.command("export")
@click.option("--output", "-o", default="-", help="Output file path (default: stdout)")
@click.option("--category", "-c", type=click.Choice(CATEGORIES), help="Filter by category")
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["jsonl", "json"]),
    default="jsonl",
    show_default=True,
    help="Output format",
)
def export_cmd(output: str, category: str, fmt: str) -> None:
    """Export benchmark tasks as JSONL or JSON (for fine-tuning / external harnesses)."""
    tasks = list_tasks(category=category)
    data = export_jsonl(tasks)

    out_str = (
        json.dumps(data, indent=2)
        if fmt == "json"
        else "\n".join(json.dumps(row) for row in data)
    )

    if output == "-":
        click.echo(out_str)
    else:
        with open(output, "w") as fh:
            fh.write(out_str)
        console.print(f"[green]Exported {len(data)} tasks → {output}[/green]")


# ──────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ──────────────────────────────────────────────────────────────────────────────


def _baseline_response_fn(task) -> str:
    """
    Trivial keyword-extraction heuristic baseline (no LLM, no API key).

    Extracts the 6 most frequent meaningful words from the input text and returns
    them as comma-separated labels.  This intentionally low bar is the floor that
    every LLM evaluation should comfortably exceed.
    """
    import re
    from collections import Counter

    # Strip common stop words to avoid meaningless matches
    stop = {
        "the", "and", "that", "this", "with", "from", "they", "have", "been",
        "their", "when", "what", "which", "were", "more", "also", "just",
        "like", "very", "some", "than", "then", "into", "your", "about",
        "would", "could", "should", "there", "really", "even", "only",
    }
    words = re.findall(r"\b[a-z]{5,}\b", task.input_text.lower())
    counts = Counter(w for w in words if w not in stop)
    candidates = [w for w, _ in counts.most_common(6)]
    return ", ".join(candidates) if candidates else "unclassified"


def _print_report(report) -> None:
    """Render a benchmark report to the terminal."""
    pass_pct = f"{report.pass_rate * 100:.0f}%"
    colour = "green" if report.pass_rate >= 0.7 else "yellow" if report.pass_rate >= 0.4 else "red"

    console.print(
        Panel(
            f"Run ID: [bold]{report.run_id}[/bold]  ·  Backend: [bold]{report.backend}[/bold]\n"
            f"Passed: {report.tasks_passed}/{report.tasks_total}  ·  "
            f"Pass rate: [{colour}]{pass_pct}[/{colour}]  ·  "
            f"Mean F1: [bold]{report.overall_f1:.3f}[/bold]",
            title="Benchmark Report",
            border_style=colour,
        )
    )

    if report.by_category:
        table = Table(box=box.SIMPLE_HEAD, title="By Category")
        table.add_column("Category", width=22)
        table.add_column("Tasks", justify="right", width=6)
        table.add_column("Passed", justify="right", width=7)
        table.add_column("Mean F1", justify="right", width=8)
        table.add_column("Pass %", justify="right", width=7)
        for cat, s in report.by_category.items():
            c = "green" if s.pass_rate >= 0.6 else "yellow" if s.pass_rate >= 0.4 else "red"
            table.add_row(
                cat.replace("_", " "),
                str(s.tasks_run),
                str(s.tasks_passed),
                f"{s.mean_f1:.3f}",
                f"[{c}]{s.pass_rate * 100:.0f}%[/{c}]",
            )
        console.print(table)

    if report.by_difficulty:
        table2 = Table(box=box.SIMPLE_HEAD, title="By Difficulty")
        table2.add_column("Difficulty", width=12)
        table2.add_column("Tasks", justify="right", width=6)
        table2.add_column("Passed", justify="right", width=7)
        table2.add_column("Mean F1", justify="right", width=8)
        diff_c_map = {"easy": "green", "medium": "yellow", "hard": "red"}
        for diff, d in report.by_difficulty.items():
            dc = diff_c_map.get(diff, "white")
            table2.add_row(
                f"[{dc}]{diff}[/{dc}]",
                str(d["tasks_run"]),
                str(d["tasks_passed"]),
                f"{d['mean_f1']:.3f}",
            )
        console.print(table2)


def _report_to_json(report) -> str:
    data = {
        "run_id": report.run_id,
        "timestamp": report.timestamp,
        "backend": report.backend,
        "tasks_total": report.tasks_total,
        "tasks_passed": report.tasks_passed,
        "pass_rate": round(report.pass_rate, 4),
        "overall_f1": report.overall_f1,
        "by_category": {
            k: {
                "tasks_run": v.tasks_run,
                "tasks_passed": v.tasks_passed,
                "mean_f1": v.mean_f1,
                "pass_rate": v.pass_rate,
            }
            for k, v in report.by_category.items()
        },
        "by_difficulty": report.by_difficulty,
        "results": [
            {
                "task_id": r.task_id,
                "category": r.category.value,
                "difficulty": r.difficulty.value,
                "passed": r.score.passed,
                "f1": r.score.f1,
                "precision": r.score.precision,
                "recall": r.score.recall,
                "predicted": r.predicted_labels,
                "raw_response": r.raw_response,
            }
            for r in report.results
        ],
    }
    return json.dumps(data, indent=2)
