from __future__ import annotations

import numpy as np


def _validated_weights(weights: np.ndarray, width: int) -> np.ndarray:
    value = np.asarray(weights, dtype=float)
    if value.ndim != 1 or len(value) != width:
        raise ValueError(f"weights must contain exactly {width} values")
    if not np.isfinite(value).all():
        raise ValueError("weights must be finite")
    if (value < 0).any():
        raise ValueError("weights must be non-negative")
    return value


def expand_group_weights(
    groups: tuple[float, float, float, float, float],
) -> np.ndarray:
    if len(groups) != 5:
        raise ValueError("Exactly five group weights are required")
    today, previous, position, volume, trend = map(float, groups)
    return _validated_weights(
        np.asarray(
            [today] * 3
            + [previous] * 3
            + [position] * 2
            + [volume, trend],
            dtype=float,
        ),
        10,
    )


def weighted_distance(vector_a, vector_b, weights) -> float:
    a = np.asarray(vector_a, dtype=float)
    b = np.asarray(vector_b, dtype=float)
    if a.ndim != 1 or b.ndim != 1 or a.shape != b.shape:
        raise ValueError("vectors must be one-dimensional and have equal length")
    weight_vector = _validated_weights(np.asarray(weights), len(a))
    delta = a - b
    return float(np.sqrt(np.sum(weight_vector * delta * delta)))


def pairwise_weighted_distances(patterns, rows, weights) -> np.ndarray:
    pattern_matrix = np.asarray(patterns, dtype=float)
    row_matrix = np.asarray(rows, dtype=float)
    if pattern_matrix.ndim != 2 or row_matrix.ndim != 2:
        raise ValueError("patterns and rows must be two-dimensional")
    if pattern_matrix.shape[1] != row_matrix.shape[1]:
        raise ValueError("patterns and rows must have the same feature width")
    weight_vector = _validated_weights(
        np.asarray(weights), pattern_matrix.shape[1]
    )

    weighted_patterns = pattern_matrix * weight_vector
    pattern_norm = np.sum(weighted_patterns * pattern_matrix, axis=1)[:, None]
    row_norm = np.sum(row_matrix * weight_vector * row_matrix, axis=1)[None, :]
    squared = pattern_norm + row_norm - 2.0 * weighted_patterns @ row_matrix.T
    return np.sqrt(np.maximum(squared, 0.0))


def is_match(distance: float, threshold: float) -> bool:
    return float(distance) <= float(threshold)
