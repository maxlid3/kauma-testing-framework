import sys
import time
import tarfile
import tempfile
import threading
import subprocess
import shutil
from pathlib import Path

import traceback

from .print_table import *

def create_tar(src_path: str, testcase_list: list):
    tmpdir = tempfile.mkdtemp()
    tar_path = Path(tmpdir) / "kauma.tar.gz"

    with tarfile.open(tar_path, "w:gz") as tar:
        for item in Path(src_path).parent.iterdir():
            tar.add(str(item), arcname=item.name)

        for item in testcase_list:
            tar.add(str(Path(item)), arcname=item.name)

    return tar_path, tmpdir

def start_container(docker_debug: bool = False):
    container_id = None
    try:
        if docker_debug:
            print("Starting Docker container 'labwork'...")
        container_id = subprocess.check_output(["docker", "run", "-dit", "labwork", "sleep", "infinity"], text=True).strip()
        if docker_debug:
            print(f"Started Docker container with id '{container_id[:13]}...'.")
        return container_id
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt.")
        if container_id is not None:
            stop_and_rm_container(container_id, docker_debug)
        else:
            print("Docker container may still be running. Please stop and remove the container manually.")
    except Exception:
        print("Error starting Docker-container. Please make sure Docker is running/installed!")
        sys.exit(1)


def stop_and_rm_container(container_id: str, docker_debug: bool = False):
    if container_id is not None:
        if docker_debug:
            print("Stopping and removing Docker container 'labwork'.")
        subprocess.run(["docker", "stop", container_id], check=True, capture_output=True)
        if docker_debug:
            print(f"Stopped Docker container with id '{container_id[:13]}...'.")
        subprocess.run(["docker", "rm", container_id], check=True, capture_output=True)
        if docker_debug:
            print(f"Removed Docker container with id '{container_id[:13]}...'.")

def make_handle_stdout(case):
    def handle_stdout(line):
        try:
            update_case(line)
        except KeyError as err:
            print(f"Missing key {err} in 'expectedResults' in case '{case}'", end='', file=sys.stderr)
        except TypeError as err:
            print(f"Wrong formatted output for case '{case}'!", end='', file=sys.stderr)
    return handle_stdout

def make_handle_stderr(traceback_str):
    def handle_stderr(line):
        if "Traceback" in line:
            traceback_str.append(line)
        elif traceback_str:
            traceback_str.append(line)
    return handle_stderr


def run_docker(kauma_path: str, testcase_list: list, debug: bool = False, docker_debug: bool = False, os_windows: bool = False):
    container_id = None
    try:
        try:
            container_id = start_container(docker_debug)
        except KeyboardInterrupt:
            print("Received KeyboardInterrupt.")
            stop_and_rm_container(container_id, docker_debug)
            sys.exit(1)


        tar_path, tmpdir = create_tar(kauma_path, testcase_list)
        
        # Copy tar archive into the container
        subprocess.run(["docker", "cp", str(tar_path), f"{container_id}:/"], check=True, capture_output=True)

        # After copying, delete the tar archive on the host
        shutil.rmtree(tmpdir)

        # Unzip tar archive in container and delete afterwards
        subprocess.run(["docker", "exec", container_id, "tar", "-xzf", "/kauma.tar.gz", "-C", "."],check=True)
        subprocess.run(["docker", "exec", container_id, "rm", "kauma.tar.gz"],check=True)
        
        if os_windows:
            subprocess.run(["docker", "exec", container_id, "chmod", "+x", "./kauma"],check=True)

        # Run the testcases and measure the time for each testcase
        print_header()
        for case in testcase_list:
            init_table_case(Path(case))

            start = time.time()

            command = ["docker", "exec", container_id, "bash", "-c", f"./kauma {case.name}"]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            traceback_str = []

            handle_stdout = make_handle_stdout(case)
            handle_stderr = make_handle_stderr(traceback_str)

            t_out = threading.Thread(target=lambda: [handle_stdout(line) for line in process.stdout])          
            t_err = threading.Thread(target=lambda: [handle_stderr(line) for line in process.stderr])

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
    except KeyboardInterrupt:
        print_debug()
        print("\nReceived KeyboardInterrupt, stopping and removing containers...")
    except Exception as err:
        print("testing-framework crashed:", err)
        traceback.print_exc()
    finally:
        if container_id is not None:
            stop_and_rm_container(container_id, docker_debug)
        sys.exit(1)

    