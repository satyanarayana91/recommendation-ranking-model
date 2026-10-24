# Recommendation Ranking Model

An end-to-end learning-to-rank project using MovieLens 100K. It ranks supplied movie candidates using historical user and item features, compares an XGBoost ranker with a popularity baseline, tracks experiments locally with MLflow, explains model scores with SHAP, and serves rankings through FastAPI.

This is an educational offline experiment, not a production recommender. The API scores candidates provided by the caller; it does not generate candidates or calculate features.

## Results

The chronological holdout experiment evaluates 829 users with at least one relevant held-out item. Ratings of 4 or 5 are considered relevant; original ratings are used as graded relevance for NDCG.

| Model | NDCG@10 | MRR@10 | MAP@10 |
| --- | ---: | ---: | ---: |
| Item-popularity baseline | 0.6158 | 0.4844 | 0.4297 |
| XGBoost `rank:ndcg` | 0.6161 | 0.5028 | 0.4442 |

The NDCG improvement is small. Candidate sets include held-out rated movies and deterministically sampled unseen movies, so these offline metrics are not a production-performance claim. See [the experiment report](reports/ranking_experiment.md) and [the assumptions and leakage review](reports/assumptions_and_leakage.md) for methodology and limitations.

## Project structure

```text
recommendation-ranking-model/
├── README.md
├── TASKS.md
├── .gitignore
├── requirements.txt
├── app.py                    # FastAPI implementation; root-level compatibility entry point
├── data/
│   └── README.md             # Dataset acquisition and storage policy
├── docs/
│   ├── PROJECT_FLOW.md       # End-to-end methodology
│   └── screenshots/
│       └── README.md         # Checklist for genuine portfolio screenshots
├── models/
│   └── README.md             # Generated model artifact policy
├── notebooks/
│   └── eda.ipynb
├── reports/                  # EDA, experiment, API demo, and analysis evidence
├── src/
│   ├── api.py                # API import path for `uvicorn src.api:app`
│   ├── evaluation.py
│   ├── features.py           # Public feature helper imports
│   ├── feature_engineering.py
│   ├── train.py              # Training entry point
│   └── ...                   # Download, EDA, demo, SHAP, SQL, and experiment scripts
└── tests/
    ├── test_api.py
    ├── test_baseline.py
    ├── test_evaluation.py
    └── test_feature_engineering.py
```

Raw and processed data, model artifacts, generated analysis artifacts, and local MLflow stores are intentionally excluded from Git. Supporting scripts and detailed generated reports remain in the repository to make the work reproducible and auditable.

## Setup and run

Use Python 3.10 or newer. From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src/download_movielens_100k.py
python -m src.run_eda
python -m src.train
python -m src.run_shap_analysis
python -m src.run_demo
python -m pytest -q
```

Training creates the local model at `artifacts/recommendation_ranker.json` and logs the run to `mlruns/`. Downloading the dataset and running the experiment are required before starting the API.

Start the API with:

```powershell
uvicorn src.api:app --reload
```

The service provides `GET /health`, `POST /rank`, and interactive documentation at `http://127.0.0.1:8000/docs`. The request must include the six historical features listed in [the project flow](docs/PROJECT_FLOW.md). A reproducible example is available in [the demo request](reports/demo_request.json) and [the demo response](reports/demo_response.json).

To view local experiment runs after training:

```powershell
mlflow ui --backend-store-uri sqlite:///mlruns/mlflow.db
```

## Data and publication

The downloader obtains MovieLens 100K directly from [GroupLens](https://grouplens.org/datasets/movielens/100k/). The dataset's attribution, redistribution, and commercial-use conditions apply. Review [data/README.md](data/README.md) and the dataset's own terms before reuse or publication. Do not commit the downloaded dataset, generated models, or local tracking databases.

## Further documentation

- [Project flow and methodology](docs/PROJECT_FLOW.md)
- [Dataset EDA](reports/dataset_eda.md)
- [SQL validation](reports/sql_validation.md)
- [Ranking experiment](reports/ranking_experiment.md)
- [MLflow tracking](reports/mlflow_tracking.md)
- [SHAP analysis](reports/shap_analysis.md)
- [Current task status](TASKS.md)

## Limitations

- Sampled unseen candidates are not confirmed negative feedback.
- The project does not implement a production candidate-retrieval system.
- Aggregate interaction features omit movie content and richer user-item compatibility.
- SHAP describes this fitted model's score behavior; it does not show causality or user preference.
- Offline results do not establish real-world recommendation quality.
