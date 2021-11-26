#!/usr/bin/env python3 

import os
import json
json_data = None

import random, string

def random_file_name(k=24):
    return "".join(random.choices(string.ascii_letters + string.digits, k=k))

with open(os.path.join(os.getcwd(), "run_settings.json"), "r") as f:
    json_data = json.load(f)

with open(os.path.join(os.getcwd(), "results_2m_gen_anf_3m5_gen_cgp/run_settings.json"), "r") as f:
    json_data_old = json.load(f)


print(len(json_data))

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