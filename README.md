# kauma-testing-framework
This is a testing framework for the TINF23CS course 'Cryptanalysis. Some testcases are provided, but you can add your own testcases at any time.

This repository is directly part of my kauma-project. That's why I will **not accept any external contributions** to my code, since only my own work shall be graded.<br>
But you can feel free using my testing-framework and modifying it for your own needs.

This testing-framework works for **Python implementations** on **Windows and Linux**. This framework does **not support compiled programming languages**.

## Prerequisites
- [Python](https://www.python.org/downloads/release/python-3140/)
- [Docker](https://www.docker.com/get-started/)
    - ["labwork" Docker-container](https://github.com/johndoe31415/labwork-docker)

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