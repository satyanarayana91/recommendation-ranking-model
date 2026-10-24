"""Generate reproducible SHAP artifacts for the saved ranking model."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mlflow
import numpy as np
import pandas as pd
import shap
from xgboost import XGBRanker

from src.run_ranking_experiment import (
    FEATURE_COLUMNS, MODEL_ARTIFACT, RANDOM_SEED, RAW_PATH, TRACKING_DATABASE,
    candidates, feature_matrix, split_per_user,
)


ARTIFACT_DIR = Path("artifacts")
REPORT_PATH = Path("reports/shap_analysis.md")
SAMPLE_SIZE = 2_000


def main() -> None:
    if not RAW_PATH.exists() or not MODEL_ARTIFACT.exists():
        raise FileNotFoundError("Run `python -m src.run_ranking_experiment` before SHAP analysis.")
    ratings = pd.read_csv(RAW_PATH, sep="\t", names=["user_id", "movie_id", "rating", "timestamp"], header=None)
    train, validation, test = split_per_user(ratings)
    history = pd.concat([train, validation], ignore_index=True)
    test_rows = feature_matrix(candidates(test, history, ratings.movie_id.unique()), history)
    test_rows = test_rows.loc[test_rows.groupby("user_id").binary_label.transform("sum") > 0].copy()
    sample = test_rows.sample(n=min(SAMPLE_SIZE, len(test_rows)), random_state=RANDOM_SEED).reset_index(drop=True)
    features = sample[FEATURE_COLUMNS]

    model = XGBRanker()
    model.load_model(str(MODEL_ARTIFACT))
    explainer = shap.TreeExplainer(model.get_booster())
    shap_values = np.asarray(explainer.shap_values(features))
    if shap_values.shape != features.shape:
        raise ValueError(f"Unexpected SHAP shape {shap_values.shape}; expected {features.shape}")

    ARTIFACT_DIR.mkdir(exist_ok=True)
    importance = pd.DataFrame({"feature": FEATURE_COLUMNS, "mean_abs_shap": np.abs(shap_values).mean(axis=0)}).sort_values("mean_abs_shap", ascending=False)
    importance_path = ARTIFACT_DIR / "shap_global_importance.csv"
    summary_path = ARTIFACT_DIR / "shap_summary.png"
    local_path = ARTIFACT_DIR / "shap_local_explanation.csv"
    importance.to_csv(importance_path, index=False)
    shap.summary_plot(shap_values, features, show=False, max_display=len(FEATURE_COLUMNS))
    plt.tight_layout()
    plt.savefig(summary_path, dpi=150, bbox_inches="tight")
    plt.close()

    scores = model.predict(features)
    local_index = int(np.argmax(scores))
    local = pd.DataFrame({"feature": FEATURE_COLUMNS, "feature_value": features.iloc[local_index].to_numpy(), "shap_value": shap_values[local_index]}).sort_values("shap_value", key=np.abs, ascending=False)
    local.insert(0, "movie_id", int(sample.iloc[local_index].movie_id))
    local.insert(0, "user_id", int(sample.iloc[local_index].user_id))
    local.insert(2, "model_score", float(scores[local_index]))
    local.to_csv(local_path, index=False)

    report = (
        "# SHAP Analysis\n\n"
        "This analysis explains XGBoost candidate **scores**, not NDCG, MRR, final rank positions, causal effects, or real-world user preference. It uses the saved model and a deterministic random sample of held-out test candidate rows.\n\n"
        f"- Model: `{MODEL_ARTIFACT}`; SHAP version: `{shap.__version__}`.\n"
        f"- Dataset: MovieLens 100K; candidate policy and relevance definition match `reports/ranking_experiment.md`.\n"
        f"- Sample: **{len(sample):,}** of **{len(test_rows):,}** test candidate rows, sampled with seed `{RANDOM_SEED}`.\n"
        f"- Features: `{', '.join(FEATURE_COLUMNS)}`.\n\n"
        "## Global mean absolute SHAP importance\n\n"
        "| Feature | Mean absolute SHAP |\n| --- | ---: |\n"
        + "".join(f"| {row.feature} | {row.mean_abs_shap:.6f} |\n" for row in importance.itertuples(index=False))
        + "\nThe table summarizes how strongly features influenced this fitted model's score across the sampled rows. It does not demonstrate causal importance or a contribution to ranking-quality improvement.\n\n"
        "## Local explanation\n\n"
        f"`artifacts/shap_local_explanation.csv` describes the highest-scoring sampled candidate (user `{int(sample.iloc[local_index].user_id)}`, movie `{int(sample.iloc[local_index].movie_id)}`). Positive SHAP values move its model score upward relative to the explainer baseline; negative values move it downward.\n\n"
        "## Limitations\n\n"
        "- Candidate sampling treats unseen movies as zero-label negatives for this educational offline experiment; this is not evidence of dislike.\n"
        "- Historical aggregate features and popularity may be correlated, so credit allocation across features should not be interpreted causally.\n"
        "- SHAP explains the fitted score function, not the validity of labels, absence of leakage, or ranking metrics. Feature ablation on the same held-out protocol is required to test whether a feature improves ranking quality.\n"
    )
    REPORT_PATH.write_text(report, encoding="utf-8")

    mlflow.set_tracking_uri(f"sqlite:///{TRACKING_DATABASE.resolve().as_posix()}")
    mlflow.set_experiment("recommendation-ranking-project")
    with mlflow.start_run(run_name="shap-history-aggregates-v1"):
        mlflow.log_params({"analysis_type": "TreeExplainer", "shap_version": shap.__version__, "explained_model": str(MODEL_ARTIFACT), "feature_version": "history-aggregates-v1", "sample_size": len(sample), "sample_seed": RANDOM_SEED})
        mlflow.log_artifact(str(importance_path))
        mlflow.log_artifact(str(summary_path))
        mlflow.log_artifact(str(local_path))
        mlflow.log_artifact(str(REPORT_PATH))
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
