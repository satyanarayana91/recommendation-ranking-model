"""A training-only, non-personalized popularity baseline."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


def item_popularity(train_interactions: pd.DataFrame) -> pd.DataFrame:
    """Count training interactions per movie; ties are deterministic by movie ID."""
    if "movie_id" not in train_interactions:
        raise ValueError("train_interactions must contain movie_id")
    return (
        train_interactions.groupby("movie_id")
        .size()
        .rename("popularity_score")
        .reset_index()
        .sort_values(["popularity_score", "movie_id"], ascending=[False, True])
        .reset_index(drop=True)
    )


def recommend_popular_unseen(
    popularity: pd.DataFrame, seen_movie_ids: Iterable[int], k: int = 10
) -> pd.DataFrame:
    """Return up to *k* popular movies after consistently removing seen items."""
    if k <= 0:
        raise ValueError("k must be positive")
    seen = set(seen_movie_ids)
    return popularity.loc[~popularity["movie_id"].isin(seen)].head(k).copy()
