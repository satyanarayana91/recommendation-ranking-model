import pandas as pd

from src.feature_engineering import attach_history_features, build_history_features


def test_history_features_are_derived_from_train_only():
    train = pd.DataFrame(
        {"user_id": [1, 1, 2], "movie_id": [10, 11, 10], "rating": [5, 3, 4]}
    )
    users, items = build_history_features(train)
    candidates = pd.DataFrame({"user_id": [1, 3], "movie_id": [10, 99]})
    featured = attach_history_features(candidates, users, items)

    assert users.loc[users.user_id == 1, "user_interaction_count"].item() == 2
    assert items.loc[items.movie_id == 10, "item_interaction_count"].item() == 2
    assert pd.isna(featured.loc[1, "user_interaction_count"])
    assert pd.isna(featured.loc[1, "item_interaction_count"])
