# Project status

This checklist reflects the implementation currently present in the repository. Screenshot captures and future experiments are intentionally marked incomplete until genuine evidence is added.

## Implemented

- [x] Select MovieLens 100K and document its source and data-handling policy.
- [x] Add a reproducible dataset downloader and exploratory data analysis.
- [x] Validate the dataset with programmatic checks and SQL.
- [x] Build chronological per-user train, validation, and test periods.
- [x] Construct historical user and item features without using held-out labels.
- [x] Implement a popularity baseline and XGBoost `rank:ndcg` experiment.
- [x] Evaluate both methods on the same per-user candidate sets with NDCG@10, MRR@10, and MAP@10.
- [x] Log experiment parameters, metrics, and artifacts to local MLflow.
- [x] Generate SHAP feature-importance and local explanation outputs.
- [x] Expose ranking through FastAPI with request validation and ranked responses.
- [x] Add tests for feature engineering, baseline behavior, evaluation metrics, and API behavior.
- [x] Add a reproducible API demo and document project methodology and limitations.

## Remaining before portfolio publication

- [ ] Capture genuine screenshots for model results, an MLflow run, and a successful API response; follow [the screenshot checklist](docs/screenshots/README.md).
- [ ] Add screenshots only after verifying their content and removing local paths or sensitive information.
- [ ] Review the final Git changes and confirm ignored data, model, and MLflow files are not staged.
- [ ] Re-run setup and documented commands in a clean environment.

## Potential improvements

- [ ] Compare candidate-generation policies using the same evaluation protocol.
- [ ] Evaluate additional content-aware or collaborative features.
- [ ] Analyze cold-start and user-segment performance.
- [ ] Add HTTP-level API tests in addition to direct endpoint tests.

## Verified metrics

Latest documented fixed-protocol results:

| Model | NDCG@10 | MRR@10 | MAP@10 |
| --- | ---: | ---: | ---: |
| Popularity baseline | 0.6158 | 0.4844 | 0.4297 |
| XGBoost ranker | 0.6161 | 0.5028 | 0.4442 |

The test set contains 829 users with at least one relevant item. These offline metrics use held-out ratings plus sampled unseen candidates; the latter are not confirmed negatives.
