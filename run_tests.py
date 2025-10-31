import sys
import argparse
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
    parser = argparse.ArgumentParser(description='kauma-testing-framework')
    parser.add_argument('kauma_path', help='Path of your kauma file')
    parser.add_argument('-d', '--debug', action='store_true', help='Activate extended debug mode')
    
    try:
        args = parser.parse_args()
    except SystemExit:
        print()
        parser.print_help()
        sys.exit(1)


    testcase_list = gen_testcase_list()
    kauma_path = Path(args.kauma_path)

    if args.debug:
        run_docker(kauma_path, testcase_list, True)
    else:
        run_docker(kauma_path, testcase_list)
