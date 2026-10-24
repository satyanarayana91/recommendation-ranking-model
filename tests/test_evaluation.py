import pytest

from src.evaluation import average_precision_at_k, ndcg_at_k, reciprocal_rank


def test_ideal_ranking_scores_one():
    labels = [3, 2, 0]
    assert ndcg_at_k(labels, 3) == pytest.approx(1.0)
    assert reciprocal_rank([1, 0, 0], 3) == pytest.approx(1.0)
    assert average_precision_at_k([1, 0, 1], 3) == pytest.approx(5 / 6)


def test_no_relevant_labels_score_zero():
    assert ndcg_at_k([0, 0], 10) == 0.0
    assert reciprocal_rank([0, 0], 10) == 0.0
    assert average_precision_at_k([0, 0], 10) == 0.0
