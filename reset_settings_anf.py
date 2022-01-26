#!/usr/bin/env python3 

import os
import json
json_data = None

import random, string

def random_file_name(k=24):
    return "".join(random.choices(string.ascii_letters + string.digits, k=k))

with open(os.path.join(os.getcwd(), "optimalization_config.json"), "r") as f:
    json_data = json.load(f)

with open(os.path.join(os.getcwd(), "optimization_arit_fce.json"), "r") as f:
    json_data_arit = json.load(f)

for record in json_data:
    record["output_file"] = random_file_name()
    record["cgp_gen"] = 11000000

for record in json_data_arit:
    record["output_file"] = random_file_name()
    record["seed_index"] = -1
    record["cgp_gen"] = 0


with open(os.path.join(os.getcwd(), "testovacka.json"), "w") as f:
    json.dump(json_data + json_data_arit , f, indent=4)
# new_json = []

# for record in json_data:
#     if record["type"] == "anf":
#         rdn_name = random_file_name()

#         file = record["output_file"]
#         prev_file = os.path.join(os.getcwd(), "outs", file)
#         new_file = os.path.join(os.getcwd(), "outs", rdn_name)

#         print(rdn_name)
#         os.rename(prev_file, new_file)
#         record["output_file"] = rdn_name
#         record["type"] = "anfN"

#         new_json.append(record)
#         #new_json.append(record)
#     # if record["type"] == "anf":
#     #     new_json.append(record)
# #     # if record["type"] == "anf" and record["gen"] == 3500000:
# #     #     file = record["output_file"]
# #     #     print(file)

# #     #     rdn_name = random_file_name()
# #     #     prev_file = os.path.join(os.getcwd(), "outs", file)
# #     #     new_file = os.path.join(os.getcwd(), "outs", rdn_name)
# #     #     print(rdn_name)
# #     #     os.rename(prev_file, new_file)
# #     #     record["output_file"] = rdn_name
# #     #     record["type"] = "anfN"


# with open(os.path.join(os.getcwd(), "run_settings.json"), "w") as f:
#     json.dump(json_data_old + new_json, f, indent=4)