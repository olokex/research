#!/usr/bin/env python3

import json, os, sys, random, string

def random_file_name(k=24):
    return "".join(random.choices(string.ascii_letters + string.digits, k=k))

data_json = []

for i in range(1000):
    name = f"func{i:0>3}"
    anf = {
        "circuit_name": name,
        "input_file": name,
        "output_file": random_file_name(),
        "arity": 6,
        "terms": 12,
        "gen": 2000000,
        "lambda": 4,
        "mutation": 2,
        "runs": 31,
        "runs_done": 0,
        "run": 0,
        "type": "anf"
    }

    cgp = {
        "circuit_name": name,
        "input_file": name,
        "output_file": random_file_name(),
        "gen": 3500000,
        "lambda": 4,
        "column": 80,
        "mutation": 2,
        "functions": "in,not,and,or,xor,nand,nor,xnor",
        "runs": 31,
        "runs_done": 0,
        "run": 0,
        "type": "cgp"
    }

    data_json.extend([anf, cgp])

with open("run_settings.json", "w") as f:
    json.dump(data_json, f, indent=4)