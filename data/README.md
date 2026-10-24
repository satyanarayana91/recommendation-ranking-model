# Data policy

Download MovieLens 100K directly from [GroupLens](https://grouplens.org/datasets/movielens/100k/) for local use:

```powershell
python src/download_movielens_100k.py
```

The downloader writes into `data/raw/`, which is intentionally ignored by Git. Do not commit or redistribute the dataset from this repository. Attribution, redistribution restrictions, and commercial-use conditions are governed by the MovieLens 100K README and GroupLens terms; review them before any use beyond this learning project.

Derived temporary data goes in `data/processed/` and is also ignored.
