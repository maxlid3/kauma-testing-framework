from print_table import *
"""
┌ - ┐
│   │
└ - ┘

┌ xxxxxxxxxxxxxxxxxxxxxxxxxxx ┐
│ xxxxxxxxxxxxxxxxxxxxxxxxxxx │
└ xxxxxxxxxxxxxxxxxxxxxxxxxxx ┘

                              .json ┌················································┐ 100.213s 5/17
                                    │················································│
                                    └················································┘
"""
import time
from pathlib import Path

print_header()
init_table_case(Path(r"testcases\calc_testcase.json"))

# 35 Zeichen pro Name
# 48 cases pro Zeile

# print("""
# ┌ - ┐
# │   │
# └ - ┘

# ┌ xxxxxxxxxxxxxxxxxxxxxxxxxxx ┐
# │ xxxxxxxxxxxxxxxxxxxxxxxxxxx │
# └ xxxxxxxxxxxxxxxxxxxxxxxxxxx ┘

#                               .json ┌\u001B[92m+++++++++++++\u001B[0m\u001B[91m---------\u001B[0m··························┐
#                                     │················································│
#                                     └················································┘      
#                               .json [\u001B[92m+++++++++++++++++++++++++++\u001B[0m\u001B[91m---\u001B[0m\u001B[92m++++++++++++++++++++\u001B[0m]
# """, end=LINE_CLEAR)

# time.sleep(2)
# print(f"""{LINE_UP}{LINE_UP}{LINE_UP}{LINE_UP}{LINE_UP}{LINE_UP}{LINE_UP}{LINE_UP}{LINE_UP}{LINE_UP}{LINE_UP}{LINE_UP}{LINE_UP}
# ┌ - ┐
# │   │
# └ - ┘

# ┌ xxxxxxxxxxxxxxxxxxxxxxxxxxx ┐
# │ xxxxxxxxxxxxxxxxxxxxxxxxxxx │
# └ xxxxxxxxxxxxxxxxxxxxxxxxxxx ┘

#                               .json ┌\u001B[92m+++++++++++++++++\u001B[0m\u001B[91m-----\u001B[0m··························┐
#                                     │················································│
#                                     └················································┘      
#                               .json [\u001B[92m+++++++++++++++++++++++++++\u001B[0m\u001B[91m---\u001B[0m\u001B[92m++++++++++++++++++++\u001B[0m]
# """, end=LINE_CLEAR)


# """
# Jetzt noch die Dinger hier

# def clear_line(n=1):
#     LINE_UP = '\033[1A'
#     LINE_CLEAR = '\x1b[2K'
#     for i in range(n):
#         print(LINE_UP, end=LINE_CLEAR)

# einbauen
# """