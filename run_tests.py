import sys
from pathlib import Path

from utils import run_docker

def gen_testcase_list():
    base = Path(__file__).parent
    testcase_list = []
    for item in Path(base / 'testcases').iterdir():
        testcase_list.append(Path(item))

    for item in Path(base / 'ext_testcases').iterdir():
        if item.name == ".gitignore":
            continue
        testcase_list.append(Path(item))

    return testcase_list

if __name__ == "__main__":
    testcase_list = gen_testcase_list()
    kauma_path = Path(sys.argv[1])

    run_docker(kauma_path, testcase_list)
