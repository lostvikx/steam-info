import os
import json

def write_info_json(appid: str, data: dict) -> None:
    data_path = f"data/{appid}.json"
    with open(data_path, "w") as f:
        json.dump(data, f, indent=4)

def read_info_json(appid: str) -> dict:
    data = dict()
    data_path = f"data/{appid}.json"

    if os.path.isfile(data_path):
        with open(data_path, "r") as f:
            data = json.load(f)
    return data
