#!/usr/bin/env python3 

import os
import json
import matplotlib.pyplot as plt
from statistics import median

PWD = os.getcwd()
OUTS_DIR = os.path.join(PWD, "out_arit_fce")
OUTS_DIR_OPT = os.path.join(PWD, "opt-outputs")

def retrieve_data(fp, search):
    data = []

    for line in fp:
        if search in line:
            _, val = line.split(": ")
            data.append(float(val))
    
    return data


def boxplot(ax, title, data, ylabel, xlabel=["CGP", "ANF"], showf=False):
    ax.set_title(title)
    ax.set_xticklabels(xlabel)
    # ax.set_xticklabels(["CGP", "ANF"])
    ax.boxplot(data, widths=0.5, showfliers=showf)
    # ax.boxplot(data, widths=0.45, showfliers=showf)
    #ax.set_yticks(yticks)
    plt.setp(ax, ylabel=ylabel)


def get(file, search):
    with open(os.path.join(OUTS_DIR, file)) as out:
        return retrieve_data(out, search)


def find_not_found(file):
    with open(os.path.join(OUTS_DIR, file)) as out:
        cnt = 0
        for line in out.readlines():
            if "NOT FOUND" in line:
                cnt += 1
        return cnt


def data_extract(file):
    data = []

    with open(os.path.join(OUTS_DIR_OPT, file)) as f:
        for line in f.readlines():
            if "CGP optimized area:" in line:
                _, area = line.split(": ")
                data.append(float(area))

    return data


with open("configuration_aritf.json") as fp:
    json_data = json.load(fp)

with open(os.path.join(PWD, "optimalization_config.json")) as f:
    json_optimized = json.load(f)


it = iter(json_data)


for cgp, anf in zip(it, it):

    opt_file = None
    for record in json_optimized:
        if record["circuit_name"] == cgp["circuit_name"]:
            opt_file = record["output_file"]
            break

    fig, axs = plt.subplots(1, 3, figsize=(16, 8), dpi=200)

    suc_cgp = (31 - find_not_found(cgp["output_file"])) / 31 * 100
    suc_anf = (31 - find_not_found(anf["output_file"])) / 31 * 100

    boxplot(axs[0], "Nalezení obvodu", 
        [get(cgp["output_file"], "evaluations:"), get(anf["output_file"], "evaluations:")], "Evaluace",
        [f"CGP\n{suc_cgp:.0f} %", f"ANF\n{suc_anf:.0f} %"])
    boxplot(axs[1], "První funkční obvod plocha",
        [get(cgp["output_file"], "first invidual area:"), get(anf["output_file"], "first invidual area:")], "Plocha $nm^2$")
    boxplot(axs[2], "Optimalizovaná plocha",
        [
        get(cgp["output_file"], "optimized area:"),
        get(anf["output_file"], "optimized area:"),
        data_extract(opt_file)
        ], "Plocha $nm^2$", xlabel=["CGP", "ANF", "ANF + CGP"])

    name = cgp["circuit_name"]
    plt.suptitle(name)
    #plt.show()
    plt.tight_layout()
    plt.savefig(f"{name}.png")
