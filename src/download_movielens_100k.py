"""Download the official MovieLens 100K rating file and its README.

The raw files are intentionally ignored by Git because the dataset terms do
not permit redistribution without separate permission.
"""

from pathlib import Path
from shutil import copyfileobj
import ssl
from urllib.request import urlopen

import certifi


DATASET_BASE_URL = "https://files.grouplens.org/datasets/movielens/ml-100k"
RAW_DATA_DIR = Path("data/raw/ml-100k")
FILES = ("u.data", "README")


def main() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    for filename in FILES:
        destination = RAW_DATA_DIR / filename
        if destination.exists():
            print(f"Already present: {destination}")
            continue
        url = f"{DATASET_BASE_URL}/{filename}"
        print(f"Downloading {url} -> {destination}")
        # Use certifi because some local Python installations have an outdated
        # operating-system certificate store. TLS verification remains enabled.
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        with urlopen(url, context=ssl_context) as response, destination.open("wb") as output:
            copyfileobj(response, output)
    print("Download complete. Review data/raw/ml-100k/README before using the data.")


if __name__ == "__main__":
    main()
