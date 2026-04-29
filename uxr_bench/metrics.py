"""Scoring metrics for the UXR Benchmark."""
from __future__ import annotations

import re


def normalise_label(label: str) -> str:
    """Lowercase, strip whitespace, replace spaces/hyphens with underscore."""
    return re.sub(r"[\s\-]+", "_", label.strip().lower())


def parse_labels(text: str) -> list[str]:
    """Parse a comma-separated (or newline-separated) label string into normalised labels."""
    if not text or not text.strip():
        return []
    parts = re.split(r"[,\n]+", text)
    result = []
    for p in parts:
        cleaned = normalise_label(p)
        if cleaned:
            result.append(cleaned)
    return result


def precision_recall_f1(
    predicted: list[str],
    ground_truth: list[str],
) -> tuple[float, float, float]:
    """Compute precision, recall, and F1 on sets of normalised string labels."""
    if not predicted and not ground_truth:
        return 1.0, 1.0, 1.0
    if not predicted:
        return 0.0, 0.0, 0.0
    if not ground_truth:
        return 0.0, 0.0, 0.0

    pred_set = set(predicted)
    gt_set = set(ground_truth)
    tp = len(pred_set & gt_set)
    precision = tp / len(pred_set)
    recall = tp / len(gt_set)
    if precision + recall == 0:
        return precision, recall, 0.0
    f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1


def _token_overlap(a: str, b: str) -> float:
    """Compute token-level overlap ratio between two underscore-delimited label strings."""
    ta = set(a.split("_"))
    tb = set(b.split("_"))
    if not ta and not tb:
        return 1.0
    intersection = ta & tb
    return len(intersection) / max(len(ta), len(tb))


def partial_match_f1(
    predicted: list[str],
    ground_truth: list[str],
    threshold: float = 0.4,
) -> tuple[float, float, float]:
    """
    F1 with partial token-overlap matching.

    A predicted label counts as a hit if it shares >= ``threshold`` token overlap
    with *any* ground-truth label.  Used for free-form insight extraction tasks
    where surface-form label wording may differ.
    """
    if not predicted and not ground_truth:
        return 1.0, 1.0, 1.0
    if not predicted:
        return 0.0, 0.0, 0.0
    if not ground_truth:
        return 0.0, 0.0, 0.0

    pred_hits = sum(
        1 for p in predicted if any(_token_overlap(p, g) >= threshold for g in ground_truth)
    )
    gt_hits = sum(
        1 for g in ground_truth if any(_token_overlap(p, g) >= threshold for p in predicted)
    )

    precision = pred_hits / len(predicted)
    recall = gt_hits / len(ground_truth)
    if precision + recall == 0:
        return precision, recall, 0.0
    f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1


def score_numeric_proximity(predicted: float, ground_truth: float, tolerance: float = 15.0) -> float:
    """
    Score a numeric prediction against a ground-truth score (0–100 range).

    Returns a 0–1 proximity score.  Full credit within *tolerance* points,
    linearly degrading to 0 at a 100-point difference.
    """
    diff = abs(predicted - ground_truth)
    if diff == 0:
        return 1.0
    if diff <= tolerance:
        # Partial credit within tolerance: max 15% penalty at the tolerance boundary
        return 1.0 - (diff / tolerance) * 0.15
    return max(0.0, 1.0 - diff / 100.0)


def extract_numeric_score(text: str) -> float | None:
    """
    Extract the first plausible 0–100 integer or float from a string.

    Returns None if no valid score is found.
    """
    if not text:
        return None
    # Match numbers 0–100 (including decimals), ignore larger numbers
    matches = re.findall(r"\b(\d{1,3}(?:\.\d+)?)\b", text)
    for m in matches:
        val = float(m)
        if 0.0 <= val <= 100.0:
            return val
    return None
