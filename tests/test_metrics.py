"""Tests for uxr_bench.metrics."""
import pytest

from uxr_bench.metrics import (
    extract_numeric_score,
    normalise_label,
    parse_labels,
    partial_match_f1,
    precision_recall_f1,
    score_numeric_proximity,
)

# ── normalise_label ────────────────────────────────────────────────────────────

def test_normalise_label_lowercase():
    assert normalise_label("Privacy") == "privacy"


def test_normalise_label_strips_whitespace():
    assert normalise_label("  trust  ") == "trust"


def test_normalise_label_replaces_spaces():
    assert normalise_label("affordance failure") == "affordance_failure"


def test_normalise_label_replaces_hyphens():
    assert normalise_label("say-do-gap") == "say_do_gap"


def test_normalise_label_mixed():
    assert normalise_label("  Notification Fatigue  ") == "notification_fatigue"


# ── parse_labels ───────────────────────────────────────────────────────────────

def test_parse_labels_simple():
    result = parse_labels("privacy, trust, control")
    assert result == ["privacy", "trust", "control"]


def test_parse_labels_newline_separated():
    result = parse_labels("privacy\ntrust\ncontrol")
    assert result == ["privacy", "trust", "control"]


def test_parse_labels_normalises():
    result = parse_labels("Privacy Concern, Trust Issue")
    assert result == ["privacy_concern", "trust_issue"]


def test_parse_labels_empty_string():
    assert parse_labels("") == []


def test_parse_labels_whitespace_only():
    assert parse_labels("   ") == []


def test_parse_labels_strips_empty_parts():
    result = parse_labels("privacy,, trust")
    assert "privacy" in result
    assert "trust" in result


# ── precision_recall_f1 ────────────────────────────────────────────────────────

def test_prf_perfect_match():
    p, r, f1 = precision_recall_f1(["a", "b"], ["a", "b"])
    assert p == pytest.approx(1.0)
    assert r == pytest.approx(1.0)
    assert f1 == pytest.approx(1.0)


def test_prf_no_overlap():
    p, r, f1 = precision_recall_f1(["x", "y"], ["a", "b"])
    assert p == 0.0
    assert r == 0.0
    assert f1 == 0.0


def test_prf_partial_overlap():
    p, r, f1 = precision_recall_f1(["a", "b", "c"], ["a", "b"])
    assert p == pytest.approx(2 / 3)
    assert r == pytest.approx(1.0)
    assert f1 > 0


def test_prf_both_empty():
    p, r, f1 = precision_recall_f1([], [])
    assert p == 1.0 and r == 1.0 and f1 == 1.0


def test_prf_empty_predicted():
    p, r, f1 = precision_recall_f1([], ["a", "b"])
    assert p == 0.0 and r == 0.0 and f1 == 0.0


def test_prf_empty_ground_truth():
    p, r, f1 = precision_recall_f1(["a"], [])
    assert p == 0.0 and r == 0.0 and f1 == 0.0


# ── partial_match_f1 ───────────────────────────────────────────────────────────

def test_partial_f1_exact_match():
    p, r, f1 = partial_match_f1(["privacy_concern"], ["privacy_concern"])
    assert f1 == pytest.approx(1.0)


def test_partial_f1_token_overlap_hits():
    # "privacy_worry" shares "privacy" with "privacy_concern" — should count as partial hit
    p, r, f1 = partial_match_f1(["privacy_worry"], ["privacy_concern"], threshold=0.4)
    assert f1 > 0


def test_partial_f1_no_overlap():
    p, r, f1 = partial_match_f1(["alpha_beta"], ["gamma_delta"], threshold=0.4)
    assert f1 == 0.0


def test_partial_f1_both_empty():
    p, r, f1 = partial_match_f1([], [])
    assert f1 == 1.0


# ── score_numeric_proximity ────────────────────────────────────────────────────

def test_proximity_exact():
    assert score_numeric_proximity(75.0, 75.0) == pytest.approx(1.0)


def test_proximity_within_tolerance():
    score = score_numeric_proximity(80.0, 75.0, tolerance=15.0)
    assert score > 0.8


def test_proximity_at_tolerance_boundary():
    score = score_numeric_proximity(90.0, 75.0, tolerance=15.0)
    assert 0.8 <= score <= 1.0


def test_proximity_far_apart():
    score = score_numeric_proximity(10.0, 90.0)
    assert score < 0.2


def test_proximity_zero():
    score = score_numeric_proximity(0.0, 100.0)
    assert score == 0.0


# ── extract_numeric_score ──────────────────────────────────────────────────────

def test_extract_integer():
    assert extract_numeric_score("Score: 82") == 82.0


def test_extract_float():
    assert extract_numeric_score("The score is 77.5") == 77.5


def test_extract_from_slash_notation():
    # "82/100" — should pick up 82 first
    result = extract_numeric_score("82/100")
    assert result == 82.0


def test_extract_none_when_no_number():
    assert extract_numeric_score("great job") is None


def test_extract_none_for_out_of_range():
    # 500 is out of 0–100 range
    assert extract_numeric_score("score is 500") is None


def test_extract_zero():
    assert extract_numeric_score("0") == 0.0


def test_extract_hundred():
    assert extract_numeric_score("100") == 100.0
