#!/usr/bin/env python3

import os
import json
import matplotlib.pyplot as plt
from statistics import median
import re

PWD = os.getcwd()
OUTS_DIR = os.path.join(PWD, "opt-outputs")


json_optimized = []

with open(os.path.join(PWD, "optimalization_config.json")) as f:
    json_optimized = json.load(f)


# a = json_optimized[0]
# print(a)

def sevenfce(filename):
    with open(os.path.join(OUTS_DIR, filename)) as f:
        reading_cgp = False
        runs = {}

        for line in f.readlines():
            if line.__contains__("========== CGP =========="):
                reading_cgp = True
            if line.__contains__("========== CGP END =========="):
                reading_cgp = False

            if not reading_cgp:
                continue

            m = re.match(R"\S+\s(\d+)\s\S+\s(\d+\.\d+)", line)
            if m:
                evo = int(m.group(1))
                area = float(m.group(2))
                # print(m.group(1), m.group(2))
                if evo in runs:
                    runs[evo].append(area)
                else:
                    runs[evo] = [area]
        
        for key, val in runs.items():
            runs[key] = sum(val) / len(runs[key])

    return runs


plt.figure(figsize=(14, 8))

for record in json_optimized:
    if record["circuit_name"].startswith("func"):
        results = sevenfce(record['output_file'])
        plt.plot(results.keys(), results.values(), label=record["circuit_name"])

 
plt.xlabel('evaluations')
plt.ylabel('area $nm^2$')
plt.title('7funcs 100 průměr')

plt.savefig("func7_out1_area.png")