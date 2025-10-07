from __future__ import annotations

import math

from src.example import normalize_scores


def test_normalize_scores_basic():
    values = [2.0, 3.0, 5.0]
    result = normalize_scores(values)
    assert math.isclose(sum(result), 1.0)
    assert result == [0.2, 0.3, 0.5]


def test_normalize_scores_zero_sum():
    values = [0.0, 0.0]
    result = normalize_scores(values)
    assert result == values
