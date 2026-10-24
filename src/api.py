"""Expose the FastAPI application and handler through ``src.api``."""

from app import (
    FEATURE_COLUMNS,
    MODEL_PATH,
    Candidate,
    RankRequest,
    RankedItem,
    RankResponse,
    app,
    health,
    rank_items,
)

__all__ = [
    "FEATURE_COLUMNS",
    "MODEL_PATH",
    "Candidate",
    "RankRequest",
    "RankedItem",
    "RankResponse",
    "app",
    "health",
    "rank_items",
]
