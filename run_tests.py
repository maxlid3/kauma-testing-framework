import sys
import argparse
import platform
from pathlib import Path

from utils import run_docker, run_nodocker

def gen_testcase_list(included_list: list, excluded_list: list) -> list:
    base = Path(__file__).parent
    testcase_list = []

    for item in Path(base / 'testcases').iterdir():
        include_match = (
            not included_list or
            any(item.name.startswith(prefix) for prefix in included_list)
        )
        exclude_match = (
            not excluded_list or
            not any(item.name.startswith(prefix) for prefix in excluded_list)
        )

        if include_match and exclude_match:
            testcase_list.append(Path(item))

    for item in Path(base / 'ext_testcases').iterdir():
        if item.name == ".gitignore":
            continue
        include_match = (
            not included_list or
            any(item.name.startswith(prefix) for prefix in included_list)
        )
        exclude_match = (
            not excluded_list or
            not any(item.name.startswith(prefix) for prefix in excluded_list)
        )

        if include_match and exclude_match:
            testcase_list.append(Path(item))

    return testcase_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage='python %(prog)s kauma_path [options]', description='kauma-testing-framework')
    parser.add_argument('kauma_path', help='Path of your kauma file')
    parser.add_argument('-d', '--debug', action='store_true', help='Activate extended debug mode')
    parser.add_argument('-dd', '--docker_debug', action='store_true', help='Enable debug messages for Docker commands')
    parser.add_argument('-nd', '--no_docker', action='store_true', help='Run testing-framework without docker.')
    parser.add_argument('-l', "--list", action='store_true', help='List all available testcases. (Useable with --include and --exclude)')
    parser.add_argument('-i', '--include', nargs='*', metavar='text', help='Filter: Include all testcases which start with <arguments>. (Useable with --exclude)')
    parser.add_argument('-e', '--exclude', nargs='*', metavar='text', help='Filter: Exclude all testcases which start with <arguments>. (Useable with --include)')
    
    try:
        args = parser.parse_args()
    except SystemExit:
        print()
        sys.exit(1)

    testcase_list = gen_testcase_list(args.include, args.exclude)
    kauma_path = Path(args.kauma_path)

    if args.list:
        for item in testcase_list:
            print(item.name)
        sys.exit(0)

    os_windows = False
    if platform.system() == "Windows":
        os_windows = True
    
    if args.no_docker:
        run_nodocker(kauma_path, testcase_list, args.debug)
    else:
        run_docker(kauma_path, testcase_list, args.debug, args.docker_debug, os_windows)
