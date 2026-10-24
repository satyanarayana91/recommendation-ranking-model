"""Per-user ranking metrics with explicit empty-label conventions."""

from __future__ import annotations

import math
from collections.abc import Iterable


def ndcg_at_k(labels: Iterable[int], k: int = 10) -> float:
    values = list(labels)[:k]
    ideal = sorted(values, reverse=True)
    dcg = sum((2**rel - 1) / math.log2(index + 2) for index, rel in enumerate(values))
    idcg = sum((2**rel - 1) / math.log2(index + 2) for index, rel in enumerate(ideal))
    return dcg / idcg if idcg else 0.0


def reciprocal_rank(labels: Iterable[int], k: int = 10) -> float:
    for index, label in enumerate(list(labels)[:k], start=1):
        if label > 0:
            return 1 / index
    return 0.0


def average_precision_at_k(labels: Iterable[int], k: int = 10) -> float:
    values = list(labels)[:k]
    relevant = sum(value > 0 for value in values)
    if not relevant:
        return 0.0
    hits = 0
    total = 0.0
    for index, label in enumerate(values, start=1):
        if label > 0:
            hits += 1
            total += hits / index
    return total / relevant
