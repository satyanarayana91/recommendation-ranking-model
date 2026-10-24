import pytest
import xgboost as xgb
from fastapi import HTTPException
from pydantic import ValidationError

from src import api as ranking_app


class FakeRanker:
    def predict(self, frame):
        return frame["item_interaction_count"].to_numpy()


@pytest.fixture
def fake_model(monkeypatch):
    monkeypatch.setattr(ranking_app.app.state, "rank_model", FakeRanker(), raising=False)


def payload():
    def features(popularity):
        return {"user_interaction_count": 12, "user_average_rating": 4.0, "user_rating_std": 1.0, "item_interaction_count": popularity, "item_average_rating": 3.5, "item_rating_std": 1.0}
    return {"user_id": "42", "top_k": 2, "candidates": [{"item_id": "10", "features": features(20)}, {"item_id": "11", "features": features(50)}, {"item_id": "12", "features": features(30)}]}


def test_rank_orders_and_limits_results(fake_model):
    response = ranking_app.rank_items(ranking_app.RankRequest.model_validate(payload()))
    assert [row.item_id for row in response.results] == ["11", "12"]
    assert [row.rank for row in response.results] == [1, 2]


def test_rank_rejects_feature_schema_mismatch(fake_model):
    request = payload()
    del request["candidates"][0]["features"]["item_rating_std"]
    with pytest.raises(HTTPException) as error:
        ranking_app.rank_items(ranking_app.RankRequest.model_validate(request))
    assert error.value.status_code == 422


def test_schema_rejects_empty_candidates():
    request = payload()
    request["candidates"] = []
    with pytest.raises(ValidationError):
        ranking_app.RankRequest.model_validate(request)


def test_real_model_artifact_inference(monkeypatch):
    model = xgb.XGBRanker()
    model.load_model(str(ranking_app.MODEL_PATH))
    monkeypatch.setattr(ranking_app.app.state, "rank_model", model, raising=False)
    response = ranking_app.rank_items(ranking_app.RankRequest.model_validate(payload()))
    assert response.returned_count == 2
    assert all(isinstance(item.score, float) for item in response.results)
