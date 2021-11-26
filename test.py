#!/usr/bin/env python3

import json, os, sys, random, string

def random_file_name(k=24):
    return "".join(random.choices(string.ascii_letters + string.digits, k=k))

data_json = []

def p():
    for i in range(1000):
        name = f"func{i:0>3}"
        anf = {
            "circuit_name": name,
            "input_file": name,
            "output_file": random_file_name(),
            "arity": 7,
            "terms": 26,
            "gen": 30000000,
            "lambda": 4,
            "mutation": 3,
            "runs": 31,
            "runs_done": 0,
            "run": 0,
            "type": "anf"
        }

        cgp = {
            "circuit_name": name,
            "input_file": name,
            "output_file": random_file_name(),
            "gen": 30000000,
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


def add_cgp(circuit, input_file, generations, column, mutation):
    cgp = {
            "circuit_name": circuit,
            "input_file": input_file,
            "output_file": random_file_name(),
            "gen": generations,
            "lambda": 4,
            "column": column,
            "mutation": mutation,
            "functions": "in,not,and,or,xor,nand,nor,xnor",
            "runs": 31,
            "runs_done": 0,
            "run": 0,
            "type": "cgp"
        }

    return cgp


def add_anf(circuit, input_file, arity, terms, generations, mutation):
    anf = {
            "circuit_name": circuit,
            "input_file": input_file,
            "output_file": random_file_name(),
            "arity": arity,
            "terms": terms,
            "gen": generations,
            "lambda": 4,
            "mutation": mutation,
            "runs": 31,
            "runs_done": 0,
            "run": 0,
            "type": "anf"
        }

    return anf

data_json.append(add_cgp("Multiplier 2x3", "multiplier2x3.pla", column=60, generations=1000000, mutation=2))
data_json.append(add_anf("Multiplier 2x3", "multiplier2x3.pla", arity=5, generations=1000000, mutation=2, terms=8))

data_json.append(add_cgp("Multiplier 3x3", "multiplier3x3.pla", column=60, generations=2000000, mutation=2))
data_json.append(add_anf("Multiplier 3x3", "multiplier3x3.pla", arity=6, generations=2000000, mutation=4, terms=16))

data_json.append(add_cgp("Multiplier 3x4", "multiplier3x4.pla", column=80, generations=10000000, mutation=3))
data_json.append(add_anf("Multiplier 3x4", "multiplier3x4.pla", arity=7, generations=10000000, mutation=4, terms=16))


data_json.append(add_cgp("Adder 2+3", "adder2_3.pla", column=50, generations=1000000, mutation=3))
data_json.append(add_anf("Adder 2+3", "adder2_3.pla", arity=5, generations=2000000, mutation=2, terms=14))

data_json.append(add_cgp("Adder 3+3", "adder3_3.pla", column=50, generations=3000000, mutation=3))
data_json.append(add_anf("Adder 3+3", "adder3_3.pla", arity=6, generations=5000000, mutation=4, terms=16))

data_json.append(add_cgp("Adder 3+4", "adder3_4.pla", column=50, generations=5000000, mutation=3))
data_json.append(add_anf("Adder 3+4", "adder3_4.pla", arity=7, generations=8000000, mutation=4, terms=16))


data_json.append(add_cgp("Median 5b", "median5.pla", column=50, generations=1000000, mutation=3))
data_json.append(add_anf("Median 5b", "median5.pla", arity=5, generations=1000000, mutation=2, terms=8))

data_json.append(add_cgp("Median 7b", "median7.pla", column=60, generations=1500000, mutation=3))
data_json.append(add_anf("Median 7b", "median7.pla", arity=7, generations=1500000, mutation=2, terms=50))


data_json.append(add_cgp("Sort 5b", "sortNet5.pla", column=60, generations=1000000, mutation=2))
data_json.append(add_anf("Sort 5b", "sortNet5.pla", arity=5, generations=1000000, mutation=2, terms=14))

data_json.append(add_cgp("Sort 6b", "sortNet6.pla", column=60, generations=1000000, mutation=2))
data_json.append(add_anf("Sort 6b", "sortNet6.pla", arity=6, generations=1000000, mutation=3, terms=26))

data_json.append(add_cgp("Sort 7b", "sortNet7.pla", column=80, generations=4000000, mutation=3))
data_json.append(add_anf("Sort 7b", "sortNet7.pla", arity=7, generations=5000000, mutation=2, terms=60))


with open("configuration_aritf.json", "w") as f:
    json.dump(data_json, f, indent=4)