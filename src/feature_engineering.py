"""Leakage-safe historical aggregate features for recommendation ranking.

Call these functions with training-period interactions only. The functions do
not inspect validation or test labels, timestamps, or ratings.
"""

from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {"user_id", "movie_id", "rating"}


def build_history_features(train_interactions: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return user and item features calculated solely from eligible history."""
    missing = REQUIRED_COLUMNS - set(train_interactions.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    user_features = (
        train_interactions.groupby("user_id")
        .agg(
            user_interaction_count=("movie_id", "size"),
            user_average_rating=("rating", "mean"),
            user_rating_std=("rating", "std"),
        )
        .reset_index()
    )
    item_features = (
        train_interactions.groupby("movie_id")
        .agg(
            item_interaction_count=("user_id", "size"),
            item_average_rating=("rating", "mean"),
            item_rating_std=("rating", "std"),
        )
        .reset_index()
    )
    return user_features, item_features


def attach_history_features(
    candidates: pd.DataFrame,
    user_features: pd.DataFrame,
    item_features: pd.DataFrame,
) -> pd.DataFrame:
    """Attach historical features to candidates without using candidate labels."""
    if not {"user_id", "movie_id"}.issubset(candidates.columns):
        raise ValueError("Candidates must contain user_id and movie_id")
    return candidates.merge(user_features, on="user_id", how="left").merge(
        item_features, on="movie_id", how="left"
    )
