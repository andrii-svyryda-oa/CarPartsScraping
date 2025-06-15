import json
from pathlib import Path

from common.settings import settings

files_dir = Path(settings.FILES_DIR)

def write_file_json_data(data: list[dict], file_path: str):
    full_path = files_dir / file_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(full_path, 'w') as f:
        json.dump(data, f)


def read_file_json_data(file_path: str) -> list[dict]:
    with open(files_dir / file_path, 'r') as f:
        return json.load(f)
