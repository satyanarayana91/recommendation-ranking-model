# SHAP Analysis

This analysis explains XGBoost candidate **scores**, not NDCG, MRR, final rank positions, causal effects, or real-world user preference. It uses the saved model and a deterministic random sample of held-out test candidate rows.

- Model: `artifacts\recommendation_ranker.json`; SHAP version: `0.54.1`.
- Dataset: MovieLens 100K; candidate policy and relevance definition match `reports/ranking_experiment.md`.
- Sample: **2,000** of **50,420** test candidate rows, sampled with seed `42`.
- Features: `user_interaction_count, user_average_rating, user_rating_std, item_interaction_count, item_average_rating, item_rating_std`.

## Global mean absolute SHAP importance

| Feature | Mean absolute SHAP |
| --- | ---: |
| item_interaction_count | 0.801980 |
| item_average_rating | 0.149270 |
| item_rating_std | 0.131921 |
| user_interaction_count | 0.063553 |
| user_rating_std | 0.039637 |
| user_average_rating | 0.029478 |

The table summarizes how strongly features influenced this fitted model's score across the sampled rows. It does not demonstrate causal importance or a contribution to ranking-quality improvement.

## Local explanation

`artifacts/shap_local_explanation.csv` describes the highest-scoring sampled candidate (user `842`, movie `50`). Positive SHAP values move its model score upward relative to the explainer baseline; negative values move it downward.

## Limitations

- Candidate sampling treats unseen movies as zero-label negatives for this educational offline experiment; this is not evidence of dislike.
- Historical aggregate features and popularity may be correlated, so credit allocation across features should not be interpreted causally.
- SHAP explains the fitted score function, not the validity of labels, absence of leakage, or ranking metrics. Feature ablation on the same held-out protocol is required to test whether a feature improves ranking quality.
