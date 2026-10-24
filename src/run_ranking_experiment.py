"""Run a reproducible MovieLens 100K ranking experiment.

The validation period supplies supervised ranker examples. Test is held out;
all test-time historical features and popularity use train + validation only.
"""

from __future__ import annotations

import json
from pathlib import Path
import time

import mlflow
import mlflow.xgboost
import numpy as np
import pandas as pd
from xgboost import XGBRanker

from src.evaluation import average_precision_at_k, ndcg_at_k, reciprocal_rank
from src.feature_engineering import attach_history_features, build_history_features


RAW_PATH = Path("data/raw/ml-100k/u.data")
REPORT_PATH = Path("reports/ranking_experiment.md")
EVALUATION_ARTIFACT = Path("reports/evaluation_report.json")
IMPORTANCE_ARTIFACT = Path("reports/feature_importance.csv")
MODEL_ARTIFACT = Path("artifacts/recommendation_ranker.json")
TRACKING_DIR = Path("mlruns")
TRACKING_DATABASE = TRACKING_DIR / "mlflow.db"
RANDOM_SEED = 42
NEGATIVES_PER_USER = 50
FEATURE_COLUMNS = [
    "user_interaction_count", "user_average_rating", "user_rating_std",
    "item_interaction_count", "item_average_rating", "item_rating_std",
]


def split_per_user(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    parts = []
    for _, group in df.sort_values(["user_id", "timestamp", "movie_id"]).groupby("user_id", sort=False):
        n = len(group)
        test_n, validation_n = max(1, n // 10), max(1, n // 10)
        labels = np.array(["train"] * (n - validation_n - test_n) + ["validation"] * validation_n + ["test"] * test_n)
        parts.append(group.assign(split=labels))
    assigned = pd.concat(parts, ignore_index=True)
    return tuple(assigned.loc[assigned.split == name].drop(columns="split") for name in ("train", "validation", "test"))


def candidates(holdout: pd.DataFrame, history: pd.DataFrame, movies: np.ndarray) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_SEED)
    rows: list[dict[str, int]] = []
    seen_by_user = history.groupby("user_id")["movie_id"].agg(set).to_dict()
    for user_id, group in holdout.groupby("user_id", sort=True):
        # Include rated holdout items; their labels come from observed ratings.
        observed = set(group.movie_id)
        seen = seen_by_user.get(user_id, set())
        eligible = np.array([movie for movie in movies if movie not in seen and movie not in observed])
        sampled = rng.choice(eligible, size=min(NEGATIVES_PER_USER, len(eligible)), replace=False)
        for row in group.itertuples(index=False):
            rows.append({"user_id": int(user_id), "movie_id": int(row.movie_id), "binary_label": int(row.rating >= 4), "graded_label": int(row.rating)})
        rows.extend({"user_id": int(user_id), "movie_id": int(movie), "binary_label": 0, "graded_label": 0} for movie in sampled)
    return pd.DataFrame(rows).sort_values(["user_id", "movie_id"]).reset_index(drop=True)


def feature_matrix(candidate_rows: pd.DataFrame, history: pd.DataFrame) -> pd.DataFrame:
    users, items = build_history_features(history)
    matrix = attach_history_features(candidate_rows, users, items)
    return matrix.fillna(0.0)


def group_sizes(df: pd.DataFrame) -> list[int]:
    sizes = df.groupby("user_id", sort=False).size().tolist()
    assert sum(sizes) == len(df)
    return sizes


def metrics(df: pd.DataFrame, score_column: str) -> dict[str, float]:
    per_user = []
    for _, group in df.groupby("user_id", sort=False):
        ranked = group.sort_values([score_column, "movie_id"], ascending=[False, True])
        if ranked.binary_label.sum() == 0:
            continue
        per_user.append((
            ndcg_at_k(ranked.graded_label.tolist(), 10),
            reciprocal_rank(ranked.binary_label.tolist(), 10),
            average_precision_at_k(ranked.binary_label.tolist(), 10),
        ))
    values = np.array(per_user)
    return {"users": int(len(values)), "ndcg_at_10": float(values[:, 0].mean()), "mrr_at_10": float(values[:, 1].mean()), "map_at_10": float(values[:, 2].mean())}


def main() -> None:
    if not RAW_PATH.exists():
        raise FileNotFoundError("Run `python src/download_movielens_100k.py` first.")
    ratings = pd.read_csv(RAW_PATH, sep="\t", names=["user_id", "movie_id", "rating", "timestamp"], header=None)
    train, validation, test = split_per_user(ratings)
    movie_ids = ratings.movie_id.unique()
    train_candidates = feature_matrix(candidates(validation, train, movie_ids), train)
    test_history = pd.concat([train, validation], ignore_index=True)
    test_candidates = feature_matrix(candidates(test, test_history, movie_ids), test_history)
    train_candidates = train_candidates.loc[train_candidates.groupby("user_id").binary_label.transform("sum") > 0].copy()
    test_candidates = test_candidates.loc[test_candidates.groupby("user_id").binary_label.transform("sum") > 0].copy()
    params = {"objective": "rank:ndcg", "n_estimators": 100, "max_depth": 5, "learning_rate": 0.05, "subsample": 0.8, "colsample_bytree": 0.8, "random_state": RANDOM_SEED, "n_jobs": 4, "eval_metric": "ndcg@10"}
    TRACKING_DIR.mkdir(exist_ok=True)
    # Override any machine-wide URI so Windows paths with spaces resolve locally.
    mlflow.set_tracking_uri(f"sqlite:///{TRACKING_DATABASE.resolve().as_posix()}")
    mlflow.set_experiment("recommendation-ranking-project")
    with mlflow.start_run(run_name="xgboost-ranker-history-aggregates-v1"):
        run_id = mlflow.active_run().info.run_id
        mlflow.log_params(params)
        mlflow.log_params({"dataset_version": "MovieLens-100K-u.data", "feature_version": "history-aggregates-v1", "label_definition": "rating>=4", "candidate_strategy": "heldout-ratings-plus-50-seeded-unseen", "split_strategy": "per-user-80-10-10-chronological", "ranking_cutoff": 10})
        ranker = XGBRanker(**params)
        start = time.perf_counter()
        ranker.fit(train_candidates[FEATURE_COLUMNS], train_candidates.binary_label, group=group_sizes(train_candidates), verbose=False)
        training_seconds = time.perf_counter() - start
        test_candidates["model_score"] = ranker.predict(test_candidates[FEATURE_COLUMNS])
        popularity = test_history.groupby("movie_id").size()
        test_candidates["popularity_score"] = test_candidates.movie_id.map(popularity).fillna(0)
        baseline = metrics(test_candidates, "popularity_score")
        model = metrics(test_candidates, "model_score")
        mlflow.log_metrics({"training_time_seconds": training_seconds, "baseline_ndcg_at_10": baseline["ndcg_at_10"], "baseline_mrr_at_10": baseline["mrr_at_10"], "baseline_map_at_10": baseline["map_at_10"], "model_ndcg_at_10": model["ndcg_at_10"], "model_mrr_at_10": model["mrr_at_10"], "model_map_at_10": model["map_at_10"], "evaluation_users": model["users"], "test_candidate_rows": len(test_candidates)})
    REPORT_PATH.write_text(
        "# Ranking Experiment\n\n"
        "This is an educational offline experiment, not a production recommendation claim. Each user's earliest 80% of interactions is history, the next 10% forms supervised training candidates, and the latest 10% is the held-out test period. Candidate sets include held-out rated movies plus 50 deterministically sampled, unseen movies per user. Sampled unobserved movies are treated as zero-label evaluation negatives for this experiment; this is a limitation, not evidence of dislike.\n\n"
        f"- Seed: `{RANDOM_SEED}`; relevance: rating >= 4; features: training-history user/item aggregates only.\n"
        f"- Raw interaction splits: train **{len(train):,}**, validation-as-training-examples **{len(validation):,}**, test **{len(test):,}**.\n"
        f"- Candidate rows: ranker training **{len(train_candidates):,}**, test **{len(test_candidates):,}**; test users with a relevant item: **{model['users']:,}**.\n\n"
        "| Method | NDCG@10 | MRR@10 | MAP@10 |\n| --- | ---: | ---: | ---: |\n"
        f"| Training-history popularity baseline | {baseline['ndcg_at_10']:.4f} | {baseline['mrr_at_10']:.4f} | {baseline['map_at_10']:.4f} |\n"
        f"| XGBoost `rank:ndcg` | {model['ndcg_at_10']:.4f} | {model['mrr_at_10']:.4f} | {model['map_at_10']:.4f} |\n\n"
        "Metrics are computed per user and averaged only over users with at least one relevant held-out rated item. NDCG uses the raw 1–5 rating for observed held-out movies and zero for sampled candidates; MRR/MAP use the fixed binary relevance policy. Both methods use exactly the same test candidate rows and seen-item exclusion.\n",
        encoding="utf-8",
    )
    EVALUATION_ARTIFACT.write_text(json.dumps({"baseline": baseline, "model": model, "training_time_seconds": training_seconds, "test_candidate_rows": len(test_candidates), "evaluation_users": model["users"]}, indent=2), encoding="utf-8")
    pd.DataFrame({"feature": FEATURE_COLUMNS, "importance": ranker.feature_importances_}).sort_values("importance", ascending=False).to_csv(IMPORTANCE_ARTIFACT, index=False)
    MODEL_ARTIFACT.parent.mkdir(exist_ok=True)
    ranker.save_model(MODEL_ARTIFACT)
    # The reports are real outputs of this run; log them together with the model.
    with mlflow.start_run(run_id=run_id):
        mlflow.log_artifact(str(REPORT_PATH))
        mlflow.log_artifact(str(EVALUATION_ARTIFACT))
        mlflow.log_artifact(str(IMPORTANCE_ARTIFACT))
        mlflow.log_artifact(str(MODEL_ARTIFACT))
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
