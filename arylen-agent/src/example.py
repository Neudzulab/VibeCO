"""Example module for Arylen Agent."""
from __future__ import annotations


def normalize_scores(scores: list[float]) -> list[float]:
    """Return scores scaled to sum to 1.0.

    Zero totals return the original list to avoid division by zero.
    """

    total = sum(scores)
    if total == 0:
        return scores
    return [value / total for value in scores]
