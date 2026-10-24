import pandas as pd

from src.baseline import item_popularity, recommend_popular_unseen


def test_popularity_ranking_filters_seen_movies_and_breaks_ties_by_id():
    train = pd.DataFrame({"movie_id": [2, 1, 2, 3, 1]})
    popularity = item_popularity(train)
    recommendations = recommend_popular_unseen(popularity, seen_movie_ids=[1], k=2)

    assert popularity.movie_id.tolist() == [1, 2, 3]
    assert recommendations.movie_id.tolist() == [2, 3]
