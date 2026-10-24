# Evidence screenshot checklist

Do not publish placeholders, generated mockups, or screenshots containing local paths, tokens, or raw MovieLens rows. Capture only genuine outputs from this repository after rerunning the commands below.

| Suggested file | Capture from | Minimum evidence |
| --- | --- | --- |
| `model-results.png` | `reports/ranking_experiment.md` | Baseline and XGBoost metrics plus the split/candidate context. |
| `mlflow-experiment.png` | Local MLflow UI after training | Experiment name, run parameters, and metrics. |
| `api-response.png` | A successful local `POST /rank` call | Request context and ranked candidates, with no sensitive/local details. |
| `dashboard.png` | Optional dashboard you actually implement | Its source, date, and displayed metric. |

Store verified captures in this folder, then add Markdown image links to the README. There are deliberately no fake PNG files here.
