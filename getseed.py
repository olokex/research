#!/usr/bin/env python3 

import os
import json
import matplotlib.pyplot as plt
from statistics import median

PWD = os.getcwd()
OUTS_DIR = os.path.join(PWD, "out_funcs7")

def retrieve_data(fp, search):
    data = []

    for line in fp:
        if search in line:
            _, val = line.split(": ")
            data.append(float(val))
    
    return data

def getseed(f):
    seeds = []
    for line in f.readlines():
        if "seed: " in line:
            _, seed = line.split(": ")
            seeds.append(int(seed))

    return seeds

with open("run_settings.json") as fp:
    json_data = json.load(fp)
    

files = {}
for record in json_data:
    if (record["type"] == "anf"):
        file = record["output_file"]
        with open(os.path.join(OUTS_DIR, file)) as f:
            files[file] = sum(retrieve_data(f, "evaluations: "))

sort_orders = sorted(files.items(), key=lambda x: x[1])

config_optimize_json = []

for file, _ in sort_orders[:100]:
    with open(os.path.join(OUTS_DIR, file)) as f:
        seeds = getseed(f)

    for rec in json_data:
        if rec["output_file"] == file:
            rec["seeds"] = seeds
            rec["resize"] = 50
            config_optimize_json.append(rec)

print(config_optimize_json)

with open("test.json", "w") as f:
    json.dump(config_optimize_json, f, indent=4)