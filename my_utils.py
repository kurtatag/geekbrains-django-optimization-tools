import json
import os

from geekshop_project.settings import BASE_DIR


def get_data_from_json(file_name: str):
    file_full_path = os.path.join(BASE_DIR, "my_data", file_name)
    with open(file_full_path, encoding='utf-8') as f:
        data = json.load(f)
    return data
