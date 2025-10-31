import time
import tarfile
import tempfile
import subprocess
import shutil
from pathlib import Path

from .print_table import *

# TODO:
#   - Handling von stdout und stderr für das framework
#   - return-Werte definieren
#   - Alle testcases im selben Docker-Container durchführen?

def create_tar(src_path: str, testcase_list: list):
    tmpdir = tempfile.mkdtemp()
    tar_path = Path(tmpdir) / "kauma.tar.gz"

    with tarfile.open(tar_path, "w:gz") as tar:
        for item in Path(src_path).parent.iterdir():
            tar.add(str(item), arcname=item.name)

        for item in testcase_list:
            tar.add(str(Path(item)), arcname=item.name)

    return tar_path, tmpdir

def start_container():
    container_id = subprocess.check_output(["docker", "run", "-dit", "labwork", "sleep", "infinity"], text=True).strip()
    return container_id

def stop_and_rm_container(container_id: str):
    subprocess.run(["docker", "stop", container_id], check=True, capture_output=True)
    subprocess.run(["docker", "rm", container_id], check=True, capture_output=True)


def run_docker(kauma_path: str, testcase_list: list):
    tar_path, tmpdir = create_tar(kauma_path, testcase_list)
    container_id = start_container()

    # Copy tar archive into the container
    subprocess.run(["docker", "cp", str(tar_path), f"{container_id}:/"], check=True, capture_output=True)

    # After copying, delete the tar archive on the host
    shutil.rmtree(tmpdir)

    # Unzip tar archive in container and delete afterwards
    subprocess.run(["docker", "exec", container_id, "tar", "-xzf", "/kauma.tar.gz", "-C", "."],check=True)
    subprocess.run(["docker", "exec", container_id, "rm", "kauma.tar.gz"],check=True)

    # Run the testcases and measure the time for each testcase
    for case in testcase_list:
        print_header()
        init_table_case(Path(case))

        start = time.time()

        command = ["docker", "exec", container_id, "bash", "-c", f"./kauma {case.name}"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)

        for line in process.stdout:
            update_case(line)

        duration = time.time() - start
        update_time(duration)

    # Stop and rm containers
    stop_and_rm_container(container_id)

    