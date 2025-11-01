from pathlib import Path
import json

json_obj = []


def init_json(file_path: Path):
    global json_obj
    with file_path.open() as file:
        json_obj = json.load(file)
    return file_path.name

def count_testcases():
    global json_obj
    return len(json_obj['testcases'].keys())

def get_case_list():
    return list(json_obj['testcases'].keys())

def get_case_result(id: str):
    return json_obj['expectedResults'][id]