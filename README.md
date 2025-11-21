# kauma-testing-framework
This is a testing framework for the TINF23CS course 'Cryptanalysis'. Some testcases are provided, but you can add your own testcases at any time. The kauma-project is tested inside the course-provided 'labwork' Docker-container, which you will need to download before using the testing-framework.

This repository is directly part of my kauma-project. That's why I will **not accept any external contributions** to my code, since only my own work shall be graded. You can still submit issues, I will fix them.<br>
But you can feel free using my testing-framework and modifying it for your own needs.

This testing-framework works for **Python implementations** on **Windows and Linux**. This framework does **not support compiled programming languages**.

## Prerequisites
- [Python](https://www.python.org/downloads/release/python-3140/)
- [Docker](https://www.docker.com/get-started/)
    - ["labwork" Docker-container](https://github.com/johndoe31415/labwork-docker)
- If testing without Docker: `pip install cryptography`

<details>
<summary>Installing the "labwork" Docker-container</summary>
If you are to lazy to open the labwork repo, here is the quick guide for the steps you need to do, for the container to work with the testing-framework.

```
$ docker pull ghcr.io/johndoe31415/labwork-docker:master
```
```
$ docker tag ghcr.io/johndoe31415/labwork-docker:master labwork
```
Running the labwork-container will be done by the testing-framework itself.
</details>

## Quick Guide
```
usage: python run_tests.py [-h] [-d] [-dd] [-nd] kauma_path

kauma-testing-framework

positional arguments:
  kauma_path           Path of your kauma file

options:
  -h, --help           show this help message and exit
  -d, --debug          Activate extended debug mode
  -dd, --docker_debug  Enable debug messages for Docker execution
  -nd, --no_docker     Run testing-framework without docker.
  -l, --list           List all available testcases. (Useable with --include and --exclude)
  -i, --include [text ...]
                        Filter: Include all testcases which start with <arguments>. (Useable with --exclude)
  -e, --exclude [text ...]
                        Filter: Exclude all testcases which start with <arguments>. (Useable with --include)
```

## Adding own testcases
The folder `testcases` has my own testcases, which I maintain. You can add your own testcases in the `ext_testcases` folder. The order of execution is `testcases` > `ext_testcases`. Make sure your testcases have `'expectedResults'` and use [this JSON-scheme](https://github.com/Sarsum/TINF23CS-kauma-tests/blob/main/schema.json) from [Sarsum/TINF23CS-kauma-tests](https://github.com/Sarsum/TINF23CS-kauma-tests/blob/main/schema.json).

## Features
### Visual representation of case results
![](https://i.imgur.com/eE76qYJ.png)


![](https://i.imgur.com/iq30Ib8.png)

### Debug-mode for debugging of testcases
![](https://i.imgur.com/2yvgmZ1.png)

## Known issues
- If the framework crashes or stops (through KeyboardInterrupt) mid-container-creation, the container will not be stopped and removed.

If you come across a framework crash, please open an issue-ticket.
