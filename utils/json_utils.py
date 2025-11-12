from pathlib import Path
from itertools import islice
import json

json_obj = []


def init_json(file_path: Path):
    global json_obj
    with file_path.open() as file:
        json_obj = json.load(file)
    return file_path.name

def count_testcases():
    global json_obj
    len_cases = len(json_obj['testcases'].keys())
    if len_cases < 1200:
        return len(json_obj['testcases'].keys())
    else:
        return 1200

def get_case_list():
    return list(islice(json_obj['testcases'].keys(), 1200))

def get_case_result(id: str):
    return json_obj['expectedResults'][id]