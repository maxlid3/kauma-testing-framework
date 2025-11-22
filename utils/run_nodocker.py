import sys
import time
import shutil
import threading
import subprocess
from pathlib import Path

from .print_table import *
from .run_docker import create_tar, make_handle_stdout, make_handle_stderr

def thread_stream(stream, callback):
    for line in stream:
        callback(line)

def rm_tmpdir(tmpdir):
    try:
        shutil.rmtree(tmpdir)
    except Exception as err:
            print("Error deleting tempdir:", err)

def run_nodocker(kauma_path: str ,testcase_list: list, debug: bool = False):
    try:
        tar_path, tmpdir = create_tar(kauma_path, testcase_list)

        subprocess.run(["tar", "-xzf", tar_path, "-C", tmpdir])

        print_header()
        for case in testcase_list:
            init_table_case(Path(case))

            start = time.time()

            command = ["python", f"{tmpdir}/kauma", f"{tmpdir}/{case.name}"]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            traceback_str = []

            handle_stdout = make_handle_stdout(case)
            handle_stderr = make_handle_stderr(traceback_str)

            t_out = threading.Thread(target=thread_stream, args=(process.stdout, handle_stdout))
            t_err = threading.Thread(target=thread_stream, args=(process.stderr, handle_stderr))
            
            t_out.start()
            t_err.start()

            t_out.join()
            t_err.join()

            # If all or the last cases are missing, one more update is needed
            update_case("{ \"id\": null, \"reply\": null }")

            duration = time.time() - start
            process.wait()
            update_time(str(round(duration, 3)) + 's')

            if debug:
                add_debug_case(''.join(traceback_str))
        if debug:
            print_debug()

        rm_tmpdir(tmpdir)

    except KeyboardInterrupt:
        print_debug()
        print("\nReceived KeyboardInterrupt.")
        rm_tmpdir(tmpdir)
    except Exception as err:
        print("testing-framework crashed:", err)
        rm_tmpdir(tmpdir)
        traceback.print_exc()
    finally:
        sys.exit(1)
