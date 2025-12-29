import os
import json
import time

def write_json(filepath:str, data:dict) -> None:
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    return None

def read_json(filepath:str) -> dict:
    data = dict()
    if os.path.isfile(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
    return data

def is_file_old(filepath:str, days=1) -> bool:
    if not os.path.isfile(filepath):
        return False
    file_time = os.path.getmtime(filepath)
    time_passed = (time.time() - file_time) / 3600
    return time_passed > 24 * days
