# Project evidence

This file points to the current, reproducible evidence for the recommendation-ranking project. It replaces the original planning checklist; the implementation and outstanding work are tracked in [TASKS.md](TASKS.md).

## Available evidence

- Dataset quality and distributions: [EDA report](reports/dataset_eda.md)
- Dataset validation queries and results: [SQL validation report](reports/sql_validation.md)
- Split, candidates, metrics, and measured results: [ranking experiment report](reports/ranking_experiment.md)
- Data assumptions and leakage controls: [assumptions and leakage review](reports/assumptions_and_leakage.md)
- Local MLflow tracking: [tracking report](reports/mlflow_tracking.md)
- Model explanations: [SHAP report](reports/shap_analysis.md)
- Request and response examples: [demo request](reports/demo_request.json), [demo response](reports/demo_response.json), and [demo run notes](reports/demo_run.md)
- Automated coverage: `tests/`

## Screenshot status

No screenshots are included yet. Only genuine captures from this project's own run should be added under `docs/screenshots/`; see its [capture checklist](docs/screenshots/README.md). Do not add placeholder images or present an unimplemented dashboard as evidence.

## Data and generated artifacts

MovieLens data is downloaded locally and ignored by Git. Generated models, SHAP outputs, and local MLflow stores are also ignored. See [data policy](data/README.md) and [model artifact policy](models/README.md).
