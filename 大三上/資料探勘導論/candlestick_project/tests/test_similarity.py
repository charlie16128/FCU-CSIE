import math

import numpy as np
import pytest

from src.similarity import (
    expand_group_weights,
    is_match,
    pairwise_weighted_distances,
    weighted_distance,
)


def test_weighted_distance_rules():
    a = np.zeros(10)
    b = np.ones(10)

    assert weighted_distance(a, a, np.ones(10)) == 0
    assert weighted_distance(a, b, np.full(10, 2.0)) > weighted_distance(
        a, b, np.ones(10)
    )
    assert math.isclose(weighted_distance(a, b, np.ones(10)), math.sqrt(10))
    assert is_match(0.5, 0.5)
    assert not is_match(0.500001, 0.5)


def test_group_weight_expansion():
    weights = expand_group_weights((1.5, 0.5, 1.0, 1.5, 2.0))

    assert weights.tolist() == [
        1.5,
        1.5,
        1.5,
        0.5,
        0.5,
        0.5,
        1.0,
        1.0,
        1.5,
        2.0,
    ]


def test_pairwise_distance_matches_scalar_calculation():
    patterns = np.asarray([[0.0] * 10, [1.0] * 10])
    rows = np.asarray([[0.5] * 10, [2.0] * 10])
    weights = np.arange(1.0, 11.0)

    matrix = pairwise_weighted_distances(patterns, rows, weights)

    for pattern_index in range(2):
        for row_index in range(2):
            assert math.isclose(
                matrix[pattern_index, row_index],
                weighted_distance(
                    patterns[pattern_index], rows[row_index], weights
                ),
            )


def test_negative_weight_is_rejected():
    with pytest.raises(ValueError, match="non-negative"):
        weighted_distance(np.zeros(10), np.ones(10), np.full(10, -1.0))
