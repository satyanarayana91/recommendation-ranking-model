# Recommendation Ranking Model — Project Flow

## Purpose

This project ranks supplied movie candidates separately for each user. It is an educational offline recommendation-ranking experiment using MovieLens 100K, not a production recommender or a search-ranking system.

```text
MovieLens ratings → validation and quality checks → chronological user holdouts
→ candidate construction → historical features → XGBoost ranker / popularity baseline
→ per-user metrics → MLflow + SHAP → FastAPI /rank → reproducible demo
```

## 1. Data and validation

The source is MovieLens 100K from GroupLens. Download it locally with `python src/download_movielens_100k.py`; raw data is excluded from Git because the source terms restrict redistribution.

The interaction schema is `user_id`, `movie_id`, `rating`, and `timestamp`. EDA verified 100,000 interactions, 943 users, 1,682 movies, no missing values, no exact duplicates, and no repeated user–movie pairs. The full evidence is in `reports/dataset_eda.md` and `reports/sql_validation.md`.

Ratings of 4 or 5 are binary relevant interactions; the original 1–5 rating is retained for graded NDCG. An unobserved movie is not assumed to be a real dislike: it is a sampled zero-label candidate only within the documented offline evaluation protocol.

## 2. Split and candidate policy

For each user, ratings are timestamp-sorted:

- Earliest 80%: historical training period.
- Next 10%: supervised ranker-training examples.
- Latest 10%: held-out test period.

For every validation/test user, a candidate group contains their held-out rated movies plus 50 deterministically sampled, unseen movies. Previously observed movies are excluded. Candidate rows are sorted by `user_id`, so each user group is contiguous and group sizes sum to the number of model rows.

This design is reproducible but limited: sampled unobserved movies are not confirmed negatives, and candidate generation is deliberately simple.

## 3. Features

Features are calculated from eligible historical interactions only. Raw IDs and labels are not model features.

| Feature | Meaning |
| --- | --- |
| `user_interaction_count` | Earlier ratings by the user |
| `user_average_rating` | Mean earlier rating by the user |
| `user_rating_std` | Standard deviation of earlier user ratings |
| `item_interaction_count` | Earlier ratings received by the movie |
| `item_average_rating` | Mean earlier movie rating |
| `item_rating_std` | Standard deviation of earlier movie ratings |

The feature helpers are in `src/feature_engineering.py`. Test-time features use training plus the earlier validation period, never test-period interactions.

## 4. Training and evaluation

Run the experiment:

```powershell
python -m src.run_ranking_experiment
```

The model is `XGBRanker(objective="rank:ndcg")`. It is trained using the validation candidate groups, then evaluated on the independent latest interaction period. The popularity baseline counts only eligible earlier interactions. Both methods use the same test candidate rows and seen-item policy.

Metrics are calculated per user and then averaged across the 829 test users with at least one relevant held-out item. The measured result from the current fixed protocol is:

| Method | NDCG@10 | MRR@10 | MAP@10 |
| --- | ---: | ---: | ---: |
| Training-history popularity | 0.6158 | 0.4844 | 0.4297 |
| XGBoost `rank:ndcg` | 0.6161 | 0.5028 | 0.4442 |

The difference is small and is not evidence of production impact. See `reports/ranking_experiment.md` for the exact counts and conventions.

## 5. MLflow and SHAP

The experiment logs actual parameters, metadata, metrics, model, evaluation JSON, feature importance, and reports to local MLflow. Open it with:

```powershell
mlflow ui --backend-store-uri sqlite:///mlruns/mlflow.db
```

Run explainability analysis after training:

```powershell
python -m src.run_shap_analysis
```

It samples 2,000 held-out candidate rows (seed 42) and generates global importance, a summary plot, and a local explanation. In this sample, `item_interaction_count` has the largest average SHAP magnitude. SHAP explains this fitted model’s scores, not causal effects, NDCG/MRR, or user preference. See `reports/shap_analysis.md`.

## 6. Serving and demo

The FastAPI endpoint scores **supplied** candidates; it does not retrieve candidates or compute features:

```powershell
uvicorn src.api:app --reload
```

`POST /rank` accepts `user_id`, `top_k`, and candidates with exactly the six listed features. It validates feature names and finite values, scores using `artifacts/recommendation_ranker.json`, sorts descending, and returns `item_id`, rank, and score. Scores are ordering scores, not probabilities. Use `/docs` at `http://127.0.0.1:8000/docs`.

To regenerate the reviewed demo request and response:

```powershell
python -m src.run_demo
```

It writes `reports/demo_request.json`, `reports/demo_response.json`, and `reports/demo_run.md` using the saved model and the same endpoint handler.

## 7. Tests and reproduction

```powershell
python -m pip install -r requirements.txt
python src/download_movielens_100k.py
python -m src.run_ranking_experiment
python -m src.run_shap_analysis
python -m src.run_demo
python -m pytest -q
```

The tests cover ranking metrics, historical feature helpers, popularity filtering, API schema failures, descending score order, top-K behavior, and real-model inference. The latest verification result is 8 passing tests.

## 8. Limitations and next steps

- MovieLens 100K is historical and does not contain exposure/impression data.
- The sampled unseen candidates are a practical evaluation convention, not real negative feedback.
- The current model lacks richer user–item compatibility features such as genre affinity.
- The API requires precomputed features and does not yet own candidate generation or feature computation.
- Offline results and SHAP do not establish real user benefit.

Next steps are candidate-policy sensitivity analysis, feature ablations, user-segment/cold-start error analysis, validation-only hyperparameter selection, and production-oriented API observability.
