#!/usr/bin/python

"""Create sample output file."""

import subprocess
import os

try:
    os.remove("sample_output.txt")
except OSError:
    pass

with open("sample_output.txt", 'a+') as sample:
    print(">python nqueen.py -h", file=sample, flush=True)
    subprocess.run(["python", "nqueen.py", "-h"],
                   shell=True,
                   stdout=sample,
                   stderr=subprocess.STDOUT)
    print(file=sample)

    print(">python nqueen.py a 1", file=sample, flush=True)
    subprocess.run(["python", "nqueen.py", "a", "1"],
                   shell=True,
                   stdout=sample,
                   stderr=subprocess.STDOUT)
    print(file=sample)

    print(">python nqueen.py 8 a", file=sample, flush=True)
    subprocess.run(["python", "nqueen.py", "8", "a"],
                   shell=True,
                   stdout=sample,
                   stderr=subprocess.STDOUT)
    print(file=sample)

    print(">python nqueen.py -1 1", file=sample, flush=True)
    subprocess.run(["python", "nqueen.py", "-1", "1"],
                   shell=True,
                   stdout=sample,
                   stderr=subprocess.STDOUT)
    print(file=sample)

    print(">python nqueen.py 8 0", file=sample, flush=True)
    subprocess.run(["python", "nqueen.py", "8", "0"],
                   shell=True,
                   stdout=sample,
                   stderr=subprocess.STDOUT)
    print(file=sample)

    print(">python nqueen.py 30 1", file=sample, flush=True)
    subprocess.run(["python", "nqueen.py", "30", "1"],
                   shell=True,
                   stdout=sample,
                   stderr=subprocess.STDOUT)
    print(file=sample)

    print(">python nqueen.py 8 1", file=sample, flush=True)
    subprocess.run(["python", "nqueen.py", "8", "1"],
                   shell=True,
                   stdout=sample,
                   stderr=subprocess.STDOUT)
    print(file=sample)

    print(">python nqueen.py --all 8 1",
          file=sample, flush=True)
    subprocess.run(["python", "nqueen.py", "--all",
                    "8", "1"],
                   shell=True,
                   stdout=sample,
                   stderr=subprocess.STDOUT)
    print(file=sample)

    print(">python nqueen.py --all --show_total_node_count 8 1",
          file=sample, flush=True)
    subprocess.run(["python", "nqueen.py", "--all", "--show_total_node_count",
                    "8", "1"],
                   shell=True,
                   stdout=sample,
                   stderr=subprocess.STDOUT)
    print(file=sample)

    print(">python nqueen.py --all --no_print --show_total_node_count 8 1",
          file=sample, flush=True)
    subprocess.run(["python", "nqueen.py", "--all",
                    "--no_print", "--show_total_node_count",
                    "8", "1"],
                   shell=True,
                   stdout=sample,
                   stderr=subprocess.STDOUT)
    print(file=sample)

    print(">python nqueen.py --show_progress --show_node_count",
          "--show_total_node_count 8 1",
          file=sample, flush=True)
    subprocess.run(["python", "nqueen.py", "--show_progress",
                    "--show_node_count",
                    "--show_total_node_count",
                    "8", "1"],
                   shell=True,
                   stdout=sample,
                   stderr=subprocess.STDOUT)
    print(file=sample)

    print(">python nqueen.py --all --no_print --show_total_node_count 12 1",
          file=sample, flush=True)
    subprocess.run(["python", "nqueen.py", "--all",
                    "--no_print", "--show_total_node_count",
                    "12", "1"],
                   shell=True,
                   stdout=sample,
                   stderr=subprocess.STDOUT)
