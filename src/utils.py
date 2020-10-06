from pathlib import Path
import json

ROOT = f"{Path(__file__).parent.parent}"
ASSETS_DIR = f"{ROOT}/assets"
DATA_DIR = f"{ASSETS_DIR}/data"
GRAPHS_DIR = f"{DATA_DIR}/graphs"
LOCAL_REPO_DIR = f"{ASSETS_DIR}/local_repo"
JSON_DIR = f"{DATA_DIR}/json"


def load_json(filename):
    with open(f"{JSON_DIR}/{filename}.json", 'r') as fp:
        data = json.load(fp)
    return data


def save_to_json(data, filename):
    with open(f"{JSON_DIR}/{filename}.json", 'w') as fp:
        json.dump(data, fp)
