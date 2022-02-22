#!/usr/bin/env python3 

import os
import json
import matplotlib.pyplot as plt
from statistics import median
import re

PWD = os.getcwd()
OUTS_DIR = os.path.join(PWD, "out_funcs7")
OUTS_DIR_OPT = os.path.join(PWD, "opt-outputs")

def retrieve_data(fp, search):
    data = []

    for line in fp:
        if search in line:
            _, val = line.split(": ")
            data.append(float(val))
    
    return data

def thousand(json_data, search, func, type):
    data = []

    for record in json_data:
        if type == record["type"]:
            with open(os.path.join(OUTS_DIR, record["output_file"])) as out_file:
                data.append(func(retrieve_data(out_file, search)))
        
    return data

def make_plot(title, min_eval, min_cost, median_eval, median_cost, showf=True):
    fig, axs = plt.subplots(2, 4, figsize=(12,6))
    plt.suptitle(title, fontsize=16)
    #plt.subplots_adjust(left=0.25)
    plt.tight_layout()

    axs[0,0].set_title('Minimální evaluace')
    axs[0,0].set_xticklabels([""])
    axs[0,0].boxplot(min_eval, widths=0.45, showfliers=showf)

    axs[1,0].set_title('Minimální cena')
    axs[1,0].set_xticklabels([""])
    axs[1,0].boxplot(min_cost, widths=0.45, showfliers=showf)

    axs[0,1].set_title('Medián evaluací')
    axs[0,1].set_xticklabels([""])
    axs[0,1].boxplot(median_eval, widths=0.45, showfliers=showf)

    axs[1,1].set_title('Medián ceny')
    axs[1,1].set_xticklabels([""])
    axs[1,1].boxplot(median_cost, widths=0.45, showfliers=showf)

    axs[0,2].set_title("test")
    axs[0,2].set_xticklabels([""])

    plt.setp(axs[0, 0], ylabel='Evaluace')
    plt.setp(axs[1, 0], ylabel='Plocha')
    plt.setp(axs[0, 1], ylabel='Evaluace')
    plt.setp(axs[1, 1], ylabel='Plocha')

    plt.show()
    #plt.savefig(f"{title}.png")


def boxplot(ax, title, data, ylabel, xticklabel=["ANF", "CGP"], showf=False):
    ax.set_title(title)
    ax.set_xticklabels(xticklabel)
    ax.boxplot(data, widths=0.45, showfliers=showf)
    # ax.boxplot(data, widths=0.45, showfliers=showf)
    #ax.set_yticks(yticks)
    plt.setp(ax, ylabel=ylabel)


def find_not_found(file):
    with open(os.path.join(OUTS_DIR, file)) as out:
        cnt = 0
        for line in out.readlines():
            if "NOT FOUND" in line:
                cnt += 1
        return cnt



with open("run_settings.json") as fp:
    json_data = json.load(fp)


with open(os.path.join(PWD, "optimalization_config.json")) as f:
    json_optimized = json.load(f)


def data_extract(file):
    data = []

    with open(os.path.join(OUTS_DIR_OPT, file)) as f:
        for line in f.readlines():
            if "CGP optimized area:" in line:
                _, area = line.split(": ")
                data.append(float(area))

    return data

def get_statistic_hundred(func):
    data = []

    for record in json_optimized:
        if record["circuit_name"].startswith("func"):
            data.append(func(data_extract(record["output_file"])))

    return data

# first = json_optimized[0]
# print(first)
# extract(first["output_file"])

    # worst_anf_max = 0
    # worst_anf_name = None
    # worst_cgp_max = 0
    # worst_cgp_name = None
    # anf = 0
    # cgp = 0

    # for record in json_data:
    
    #     with open(os.path.join(OUTS_DIR, record["output_file"])) as out_file:
    #         out = find_not_found(out_file)

    #         if out:

    #             if record["type"] == "anf":
    #                 anf += out
    #                 if out > worst_anf_max:
    #                     worst_anf_max = out
    #                     worst_anf_name = record["output_file"]
    #             else:
    #                 if out > worst_cgp_max:
    #                     worst_cgp_max = out
    #                     worst_cgp_name = record["output_file"]
    #                 cgp += out

    # print(m)
    # print("anf", anf, f"worst {worst_anf_max} file: {worst_anf_name}")
    # # print(sorted(worst))
    # print("cgp", cgp, f"worst {worst_cgp_max} file: {worst_cgp_name}")

    # exit()
anf_not_found = 0
for record in json_data:
    if record["type"] == "anf":
        anf_not_found += find_not_found(record["output_file"])

cgp_not_found = 0
for record in json_data:
    if record["type"] == "cgp":
        cgp_not_found += find_not_found(record["output_file"])      

anf_not_found = 100 - anf_not_found / 31000 * 100
cgp_not_found = 100 - cgp_not_found / 31000 * 100


min_anf = median(thousand(json_data, "evaluations:", min, "anf"))
min_cgp = median(thousand(json_data, "evaluations:", min, "cgp"))

med_anf = median(thousand(json_data, "evaluations:", median, "anf"))
med_cgp = median(thousand(json_data, "evaluations:", median, "cgp"))

print("anf min avg: ", min_anf)
print("cgp min avg: ", min_cgp)
print("anf faster min ", min_cgp//min_anf)
print()
print("anf med avg: ", med_anf)
print("cgp med avg: ", med_cgp)
print("anf faster med ", med_cgp/med_anf)

fig, axs = plt.subplots(2, 2, figsize=(12, 8), dpi=200)
# fig, axs = plt.subplots(2, 4, figsize=(12,6))
plt.suptitle("Porovnání ANF/CGP 1000 Funkcí 7 Vstupů 31 Běhů Očištěné", fontsize=16)
#plt.tight_layout()


lst = list(range(10))
props = dict(boxstyle='square', facecolor='white', alpha=0.5)
txt_min = f"median\nanf {min_anf:.0f}\ncgp {min_cgp:.0f}\nANF urychlení {min_cgp/min_anf:.0f} krát"
axs[0,0].text(0.05, 0.95, txt_min, transform=axs[0,0].transAxes, fontsize=8,
    verticalalignment='top', bbox=props)

txt_med = f"median\nanf {med_anf:.0f}\ncgp {med_cgp:.0f}\nANF urychlení {med_cgp/med_anf:.0f} krát"
axs[0,1].text(0.05, 0.95, txt_med, transform=axs[0,1].transAxes, fontsize=8,
    verticalalignment='top', bbox=props)

boxplot(axs[0,0], "Minimální evaluace", 
    [thousand(json_data, "evaluations:", min, "anf"), 
    thousand(json_data, "evaluations:", min, "cgp")], "Evaluace",
    xticklabel=[f"ANF\n{anf_not_found:.0f} %", f"CGP\n{cgp_not_found:.0f} %"])

boxplot(axs[0,1], "Medián evaluací", 
    [thousand(json_data, "evaluations:", median, "anf"),
    thousand(json_data, "evaluations:", median, "cgp")], "Evaluace")

boxplot(axs[1,0], "Minimální cena", 
    [
        thousand(json_data, "optimized area:", min, "anf"), 
        thousand(json_data, "optimized area:", min, "cgp"),
        get_statistic_hundred(min)
    ], "Plocha", xticklabel=["ANF", "CGP", "ANF + CGP"])

boxplot(axs[1,1], "Medián ceny",
    [
        thousand(json_data, "optimized area:", median, "anf"),
        thousand(json_data, "optimized area:", median, "cgp"),
        get_statistic_hundred(median)
    ], "Plocha", xticklabel=["ANF", "CGP", "ANF + CGP"])

#plt.subplot_tool()
# plt.show()
plt.savefig("porovnani_fun7_anf_cgp_ocistene.png")

