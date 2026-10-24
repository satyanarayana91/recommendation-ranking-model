# Model artifacts

Training writes the local XGBoost ranker to `artifacts/recommendation_ranker.json`. It is excluded from Git because it is generated from MovieLens-derived training data.

Recreate it locally from the repository root with:

```powershell
python -m src.train
```

The FastAPI service loads that artifact at startup. Run training before starting `uvicorn src.api:app --reload`.
