import json
from pathlib import Path


BASE_PATH = Path(__file__).resolve().parent / "data"


def read_file(file_name):
    path = BASE_PATH / file_name

    with path.open(mode="r", encoding="utf-8") as file:
        return json.load(file)