#!/usr/bin/env python3

import json, os, sys
import subprocess
import time
import json
import shutil

def runner(config_file, outsdir):
    settings = []
    proclist = []
    next_setting = 0

    def spawn_process(d):
        if d['type'] == 'cgp':
            print(f"running {d['circuit_name']}")
            template = f"./build/cgp path ./data/{d['input_file']} generations {d['gen']} second-criterion true column {d['column']} lambda {d['lambda']} mutate {d['mutation']} functions {d['functions']}"
            out = f"./{outsdir}/{d['output_file']}"
            outfile = open(out, 'a')
            p = subprocess.Popen(template, shell=True, stdout=outfile, stderr=outfile)
            return p
        elif d['type'] == 'anf':
            print(f"running {d['circuit_name']}")
            template = f"./build/anf path ./data/{d['input_file']} generations {d['gen']} second-criterion true arity {d['arity']} terms {d['terms']} lambda {d['lambda']} mutate {d['mutation']}"
            out = f"./{outsdir}/{d['output_file']}"
            outfile = open(out, 'a')
            p = subprocess.Popen(template, shell=True, stdout=outfile, stderr=outfile)
            return p
        else:
            print('neznam typ ' + d['type'])

    def load_settings():
        nonlocal settings
        with open(config_file, 'r') as outfile:
            settings = json.load(outfile)
        for s in settings:
            if not 'runs_done' in s:
                s['runs_done'] = 0
            s['run'] = s['runs_done']

    def save_settings():
        shutil.copy(config_file, config_file + '.bak')
        with open(config_file, 'w') as outfile:
            json.dump(settings, outfile, indent=4)

    def get_next_setting():
        nonlocal next_setting
        n = 0
        while settings[next_setting]['run'] >= settings[next_setting]['runs']:
            next_setting = (next_setting + 1) % len(settings)
            n += 1
            if n > len(settings):
                return None
        settings[next_setting]['run'] += 1
        setting = settings[next_setting]
        next_setting = (next_setting + 1) % len(settings)
        print(setting['run'], setting['runs'])
        return setting

    load_settings()

    if not os.path.exists(outsdir):
        os.mkdir(outsdir)

    while True:
        no_settings = False
        while len(proclist) < 12:
            s = get_next_setting()
            if not s:
                no_settings = True
                break
            p = spawn_process(s)
            proclist.append((p, s))
        if no_settings and not proclist:
            break
        time.sleep(1)
        ended = []
        for p in proclist:
            if p[0].poll() != None:
                print("process ended")
                ended.append(p)
        for p in ended:
            p[1]['runs_done'] += 1
            proclist.remove(p)
        save_settings()
        
    print('all finished')




def print_circuits(config_file):
    crc = []
    with open(config_file, 'r') as outfile:
        settings = json.load(outfile)
        for setting in settings:
            if setting["circuit_name"] not in crc:
                crc.append(setting["circuit_name"])
    for each in crc:
        print(each)

runner("configuration_aritf.json", "out_arit_fce")
