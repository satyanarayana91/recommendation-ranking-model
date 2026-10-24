"""FastAPI serving layer for the saved MovieLens ranking experiment."""

from contextlib import asynccontextmanager
import math
from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator


MODEL_PATH = Path("artifacts/recommendation_ranker.json")
FEATURE_COLUMNS = [
    "user_interaction_count",
    "user_average_rating",
    "user_rating_std",
    "item_interaction_count",
    "item_average_rating",
    "item_rating_std",
]


class Candidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    item_id: str = Field(min_length=1)
    features: dict[str, float]

    @field_validator("item_id")
    @classmethod
    def non_blank_item(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("item_id must not be blank")
        return value

    @field_validator("features")
    @classmethod
    def finite_features(cls, value: dict[str, float]) -> dict[str, float]:
        if not value:
            raise ValueError("features must not be empty")
        if any(not name.strip() or not math.isfinite(number) for name, number in value.items()):
            raise ValueError("feature names must be non-blank and values must be finite")
        return value


class RankRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    user_id: str = Field(min_length=1)
    candidates: list[Candidate] = Field(min_length=1)
    top_k: int = Field(default=10, ge=1)

    @field_validator("user_id")
    @classmethod
    def non_blank_user(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("user_id must not be blank")
        return value


class RankedItem(BaseModel):
    item_id: str
    rank: int
    score: float


class RankResponse(BaseModel):
    user_id: str
    results: list[RankedItem]
    returned_count: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not MODEL_PATH.is_file():
        raise RuntimeError(f"Trained model not found: {MODEL_PATH}. Run the ranking experiment first.")
    model = xgb.XGBRanker()
    model.load_model(str(MODEL_PATH))
    app.state.rank_model = model
    yield


app = FastAPI(title="Recommendation Ranking API", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/rank", response_model=RankResponse)
def rank_items(request: RankRequest) -> RankResponse:
    expected = set(FEATURE_COLUMNS)
    for candidate in request.candidates:
        received = set(candidate.features)
        if missing := expected - received:
            raise HTTPException(422, {"item_id": candidate.item_id, "missing_features": sorted(missing), "unexpected_features": sorted(received - expected)})
        if unexpected := received - expected:
            raise HTTPException(422, {"item_id": candidate.item_id, "missing_features": [], "unexpected_features": sorted(unexpected)})
    matrix = pd.DataFrame([{name: candidate.features[name] for name in FEATURE_COLUMNS} for candidate in request.candidates], columns=FEATURE_COLUMNS)
    if not np.isfinite(matrix.to_numpy(dtype=float)).all():
        raise HTTPException(422, "All feature values must be finite")
    try:
        scores = app.state.rank_model.predict(matrix)
    except Exception as exc:
        raise HTTPException(500, "Ranking inference failed") from exc
    scored = [{"item_id": candidate.item_id, "score": float(score)} for candidate, score in zip(request.candidates, scores)]
    if any(not math.isfinite(item["score"]) for item in scored):
        raise HTTPException(500, "Model produced a non-finite score")
    scored.sort(key=lambda item: item["score"], reverse=True)
    results = [RankedItem(item_id=item["item_id"], score=item["score"], rank=index) for index, item in enumerate(scored[:request.top_k], start=1)]
    return RankResponse(user_id=request.user_id, results=results, returned_count=len(results))
