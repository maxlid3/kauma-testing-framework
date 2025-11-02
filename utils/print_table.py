import json
from pathlib import Path

from .json_utils import *

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'
LINE_RED = '\033[91m'
LINE_GREEN = '\033[92m'
LINE_COLOR_END = '\033[0m'

MAX_NAME_LEN = 35
MAX_CASES_LEN = 48 # per line

case_count = 0
line_count = 0

case_index = 0
line_index = 0
passed_count = 0
failed_list = []
missing_list = []
prev_sum_of_symbols = 0
case_list = []

debug_str = ''

name_str = ''
cases_str_list = []
time_str = ''
success_str = ''

def line_clear():
    print(LINE_CLEAR, end='', flush=True)

def line_up(n: int):
    print(LINE_UP * n, end='', flush=True)

def check_result():
    return 0

def print_header():
    print('Name'.center(35)  + '|' + 'Cases'.center(50) + '|' + 'Time'.center(8) + '|' + ' Successful/Total % (Missing)', flush=True)

def init_table_case(file_path: Path):
    global case_count
    global line_count

    global case_index
    global line_index
    global passed_count
    global failed_list
    global missing_list
    global prev_sum_of_symbols
    global case_list

    global name_str
    global cases_str_list
    global time_str
    global success_str

    file_name = init_json(file_path).center(35)
    if len(file_name) > MAX_NAME_LEN:
        file_name = file_name[0:-3] + '...'

    case_count = count_testcases()
    line_count = (case_count // MAX_CASES_LEN) + 1

    case_index = 0
    line_index = 0
    passed_count = 0
    failed_list = []
    missing_list = []
    prev_sum_of_symbols = 0
    case_list = get_case_list()

    name_str = file_name.ljust(MAX_NAME_LEN)
    time_str = ''.ljust(8)
    cases_str_list = []
    success_str = ' ' + ('0' + '/' + f'{case_count}').ljust(9) + ' ' + '0.00%'.ljust(7) + ' ' + '(' + '0' + ')'
    if line_count == 1:
        cases_str_list.append(('['+ ('·' * case_count) + ']').ljust(MAX_CASES_LEN + 2))
    if line_count > 1:
        for line in range(line_count):
            if line == 0:
                cases_str_list.append('┌' + ('·' * MAX_CASES_LEN) + '┐')
            elif line == (line_count - 1):
                cases_str_list.append('└' + (('·' * (case_count - (line * MAX_CASES_LEN))).ljust(MAX_CASES_LEN)) + '┘')
            else:
                cases_str_list.append('│' + ('·' * MAX_CASES_LEN) + '│')
    
    print(name_str + ' ' + cases_str_list[0] + ' ' + time_str + ' ' + success_str, end='\n', flush=True)
    
    if len(cases_str_list) > 1:
        for i in range(1, len(cases_str_list[1:]) + 1):
            print((' ' * len(name_str)) + ' ' + cases_str_list[i] + ' ' + (' ' * len(time_str)) + ' ' + (' ' * len(success_str)), end='\n', flush=True)


def update_case(output: str):
    global case_count
    global line_count

    global case_index
    global line_index
    global passed_count
    global failed_list
    global missing_list
    global prev_sum_of_symbols
    global case_list

    global name_str
    global cases_str_list
    global time_str
    global success_str

    output_obj = json.loads(output)
    output_id = output_obj['id']
    output_reply = output_obj['reply']


    found = False
    while found == False:
        if case_index >= case_count:
            return None
        elif output_id != case_list[case_index]:
            missing_list.append(case_list[case_index])
            case_index += 1
            continue
        else:
            found = True

    if output_id == case_list[case_index]:
        if output_reply == get_case_result(case_list[case_index]):
            new_str = LINE_GREEN + '+' + LINE_COLOR_END
        else:
            new_str = LINE_RED + '-' + LINE_COLOR_END
    

    line_index = (case_index) // MAX_CASES_LEN
    case_str_index = (case_index - (line_index * MAX_CASES_LEN)) + (((passed_count + len(failed_list)) * 9) - prev_sum_of_symbols)

    if new_str == (LINE_GREEN + '+' + LINE_COLOR_END):
        if cases_str_list[line_index][1 + case_str_index - 10:1 + case_str_index] == (LINE_GREEN + '+' + LINE_COLOR_END):
            new_cases_str = cases_str_list[line_index][:1 + case_str_index] + new_str + cases_str_list[line_index][1 + case_str_index + 1:]
            passed_count += 1
            case_index += 1
        else:
            new_cases_str = cases_str_list[line_index][:1 + case_str_index] + new_str + cases_str_list[line_index][1 + case_str_index + 1:]
            passed_count += 1
            case_index += 1

    if new_str == (LINE_RED + '-' + LINE_COLOR_END):
        if cases_str_list[line_index][1 + case_str_index - 10:1 + case_str_index] == (LINE_RED + '-' + LINE_COLOR_END):
            new_cases_str = cases_str_list[line_index][:1 + case_str_index] + new_str + cases_str_list[line_index][1 + case_str_index + 1:]
            failed_list.append('\'' + output_id + '\'')
            case_index += 1
        else:
            new_cases_str = cases_str_list[line_index][:1 + case_str_index] + new_str + cases_str_list[line_index][1 + case_str_index + 1:]
            failed_list.append('\'' + output_id + '\'')
            case_index += 1

    cases_str_list[line_index] = new_cases_str
    success_str = ' ' + (f'{passed_count}' + '/' + f'{case_count}').ljust(9) + ' ' + f'{round(((passed_count / case_count) * 100), 2)}%'.ljust(7) + ' ' + '(' + str(len(missing_list)) + ')'
    
    print(LINE_UP * line_count, end='\r', flush=True)
    print(LINE_CLEAR + name_str + ' ' + cases_str_list[0] + ' ' + time_str + ' ' + success_str, end='\n', flush=True)

    for i in range(1, len(cases_str_list[1:]) + 1):
        print((' ' * len(name_str)) + ' ' + cases_str_list[i] + ' ' + (' ' * len(time_str)) + ' ' + (' ' * len(success_str)), end='\n', flush=True)

    if case_index % 48 == 0:
        prev_sum_of_symbols = (passed_count + len(failed_list)) * 9

def update_time(time: str):
    global line_count

    global name_str
    global cases_str
    global time_str
    global success_str

    time_str = time.center(8)
    success_str = ' ' + (f'{passed_count}' + '/' + f'{case_count}').ljust(9) + ' ' + f'{round(((passed_count / case_count) * 100), 2)}%'.ljust(7) + ' ' + '(' + str(len(missing_list)) + ')'

    print(LINE_UP * line_count, end='\r', flush=True)
    print(LINE_CLEAR + name_str + ' ' + cases_str_list[0] + ' ' + time_str + ' ' + success_str, end='\n', flush=True)

    for i in range(1, len(cases_str_list[1:]) + 1):
        print((' ' * len(name_str)) + ' ' + cases_str_list[i] + ' ' + (' ' * len(time_str)) + ' ' + (' ' * len(success_str)), end='\n', flush=True)

def add_debug_case():
    global name_str
    global failed_list
    global missing_list

    global debug_str

    name = name_str.strip()
    debug_str += f'{name}:\n    Failed:  {(', '.join(failed_list)) if failed_list else 'None'}\n    Missing: {(', '.join(missing_list)) if missing_list else 'None'}\n'

def print_debug():
    print('-' * 125, flush=True)
    print(debug_str, flush=True)
