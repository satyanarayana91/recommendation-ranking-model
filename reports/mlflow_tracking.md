# MLflow Experiment Tracking

`python -m src.run_ranking_experiment` creates a local MLflow run in the `recommendation-ranking-project` experiment. Its tracking database is `mlruns/mlflow.db` and is intentionally ignored by Git.

Each run records the real ranking experiment's XGBoost parameters, dataset identifier, feature version, label rule, candidate strategy, chronological split, ranking cutoff, training time, baseline metrics, model metrics, evaluation-user count, and test-candidate count.

Artifacts produced and logged by the run:

- `reports/recommendation_ranker.json` — the actual XGBoost model.
- `reports/evaluation_report.json` — measured metrics and counts.
- `reports/feature_importance.csv` — model feature importance.
- `reports/ranking_experiment.md` — experiment methodology, results, and limitations.

To inspect the local run in the MLflow UI after rerunning the experiment:

```powershell
mlflow ui --backend-store-uri sqlite:///mlruns/mlflow.db
```

Then open `http://127.0.0.1:5000`. MLflow records provenance; it does not by itself prove that the candidate policy or offline metrics represent production performance.
