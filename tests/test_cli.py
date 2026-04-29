"""Tests for uxr_bench.cli."""
import json

import pytest
from click.testing import CliRunner

from uxr_bench.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


# ── list ───────────────────────────────────────────────────────────────────────

def test_list_default(runner):
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "TC-001" in result.output


def test_list_shows_25_tasks(runner):
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    # Count task IDs (rough check)
    assert result.output.count("TC-") + result.output.count("BD-") + \
           result.output.count("IE-") + result.output.count("GE-") + \
           result.output.count("SD-") >= 25


def test_list_category_filter(runner):
    result = runner.invoke(cli, ["list", "--category", "bias_detection"])
    assert result.exit_code == 0
    assert "BD-001" in result.output
    assert "TC-001" not in result.output


def test_list_difficulty_filter(runner):
    result = runner.invoke(cli, ["list", "--difficulty", "easy"])
    assert result.exit_code == 0
    assert "easy" in result.output.lower()


def test_list_tag_filter(runner):
    result = runner.invoke(cli, ["list", "--tag", "fintech"])
    assert result.exit_code == 0
    # Should return some tasks (at least 1 fintech-tagged task exists)
    assert "task(s)" in result.output.lower() or "TC-" in result.output or "BD-" in result.output


def test_list_json_output(runner):
    result = runner.invoke(cli, ["list", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert isinstance(data, list)
    assert len(data) == 25
    assert "task_id" in data[0]


def test_list_json_category_filter(runner):
    result = runner.invoke(cli, ["list", "--category", "thematic_coding", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert len(data) == 5
    assert all(d["category"] == "thematic_coding" for d in data)


def test_list_unknown_tag_empty(runner):
    result = runner.invoke(cli, ["list", "--tag", "zzz_nonexistent"])
    assert result.exit_code == 0


# ── show ───────────────────────────────────────────────────────────────────────

def test_show_valid_task(runner):
    result = runner.invoke(cli, ["show", "TC-001"])
    assert result.exit_code == 0
    assert "TC-001" in result.output


def test_show_case_insensitive(runner):
    result = runner.invoke(cli, ["show", "tc-001"])
    assert result.exit_code == 0
    assert "TC-001" in result.output


def test_show_invalid_task(runner):
    result = runner.invoke(cli, ["show", "XX-999"])
    assert result.exit_code != 0


def test_show_json_output(runner):
    result = runner.invoke(cli, ["show", "GE-001", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["task_id"] == "GE-001"
    assert "category" in data
    assert "ground_truth_labels" in data


# ── stats ──────────────────────────────────────────────────────────────────────

def test_stats_default(runner):
    result = runner.invoke(cli, ["stats"])
    assert result.exit_code == 0
    assert "25" in result.output


def test_stats_json_output(runner):
    result = runner.invoke(cli, ["stats", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["total"] == 25
    assert "by_category" in data
    assert "by_difficulty" in data


# ── export ─────────────────────────────────────────────────────────────────────

def test_export_jsonl_default(runner):
    result = runner.invoke(cli, ["export"])
    assert result.exit_code == 0
    lines = [line for line in result.output.strip().splitlines() if line.strip()]
    assert len(lines) == 25
    row = json.loads(lines[0])
    assert "task_id" in row


def test_export_json_format(runner):
    result = runner.invoke(cli, ["export", "--format", "json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert isinstance(data, list)
    assert len(data) == 25


def test_export_category_filter(runner):
    result = runner.invoke(cli, ["export", "--category", "say_do_gap"])
    assert result.exit_code == 0
    lines = [line for line in result.output.strip().splitlines() if line.strip()]
    assert len(lines) == 5
    for line in lines:
        row = json.loads(line)
        assert row["category"] == "say_do_gap"


def test_export_to_file(runner, tmp_path):
    out = tmp_path / "bench.jsonl"
    result = runner.invoke(cli, ["export", "-o", str(out)])
    assert result.exit_code == 0
    assert out.exists()
    lines = out.read_text().strip().splitlines()
    assert len(lines) == 25


# ── run ────────────────────────────────────────────────────────────────────────

def test_run_single_task_baseline(runner):
    result = runner.invoke(cli, ["run", "--task", "TC-001"])
    assert result.exit_code == 0
    assert "baseline" in result.output.lower() or "report" in result.output.lower()


def test_run_single_task_json(runner):
    result = runner.invoke(cli, ["run", "--task", "BD-001", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert isinstance(data, dict)
    assert "backend" in data or "results" in data or "task_id" in data


def test_run_category(runner):
    result = runner.invoke(cli, ["run", "--category", "guide_evaluation"])
    assert result.exit_code == 0
    assert "guide" in result.output.lower() or "report" in result.output.lower()


def test_run_category_difficulty(runner):
    result = runner.invoke(cli, ["run", "--category", "thematic_coding", "--difficulty", "easy"])
    assert result.exit_code == 0
    assert "thematic" in result.output.lower() or "report" in result.output.lower()


def test_run_all_baseline(runner):
    result = runner.invoke(cli, ["run", "--all"])
    assert result.exit_code == 0
    # Should show summary
    assert "pass" in result.output.lower() or "score" in result.output.lower()


def test_run_invalid_task(runner):
    result = runner.invoke(cli, ["run", "--task", "ZZ-999"])
    assert result.exit_code != 0


def test_run_no_flags(runner):
    result = runner.invoke(cli, ["run"])
    assert result.exit_code != 0
