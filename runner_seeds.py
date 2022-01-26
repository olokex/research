import json
import subprocess
import shutil
import copy
import time
import os
import re

output_dir = './opt-outputs/'

class RunSettings:
    def __init__(self, run_settings_filename):
        self.run_settings_filename = run_settings_filename
        self.setting_index = -1
        self.load()
    
    def load(self):
        with open(self.run_settings_filename, 'r') as f:
            self.run_settings = json.load(f)
        for i in range(len(self.run_settings)):
            if 'seed_index_finished' in self.run_settings[i]:
                self.run_settings[i]['seed_index'] = self.run_settings[i]['seed_index_finished']
            else:
                self.run_settings[i]['seed_index'] = -1
    
    def save(self):
        shutil.copyfile(self.run_settings_filename, self.run_settings_filename + '.bak')
        with open(self.run_settings_filename, 'w') as f:
            json.dump(self.run_settings, f, indent=4)

    def get_next_setting(self):
        attempts = 0
        while attempts < len(self.run_settings):
            self.setting_index += 1
            if self.setting_index >= len(self.run_settings):
               self.setting_index = 0
               continue 
            setting = copy.deepcopy(self.run_settings[self.setting_index])
            seed_index = setting['seed_index'] + 1
            if seed_index == len(setting['seeds']):
                attempts += 1
                continue
            setting['setting_index'] = self.setting_index
            setting['seed_index'] = seed_index
            setting['seed'] = setting['seeds'][seed_index]
            del setting['seeds']
            self.run_settings[self.setting_index]['seed_index'] = seed_index
            return setting
        return None
    
    def finish_setting(self, setting):
        self.run_settings[setting['setting_index']]['seed_index_finished'] = setting['seed_index']
        self.save()

class Process:
    def __init__(self, setting):
        self.setting = setting
        self.finished = False
        self.stage = 0
        self.n_stages = 2
    
    def start(self):
        circuit = ""
        if self.stage == 0:
            print(f"Starting {self.setting['circuit_name']}")
            args = (f"./build/anf path ./data/{self.setting['input_file']} generations {self.setting['gen']} arity "
                    f"{self.setting['arity']} terms {self.setting['terms']} mutate {self.setting['mutation']} print-cgp true")
            output_filename = f"{output_dir}/{self.setting['output_file']}"
            output_file = open(output_filename, 'a')
            self.proc = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=output_file)
            std_out = self.proc.stdout.read().decode('UTF-8') 
            output_file.write(std_out)
            print(std_out)
            regex = re.findall(R"\{.*\)", std_out)
            circuit = regex[0].strip()
        elif self.stage == 1:
            print(f"Starting CGP optimization {self.setting['circuit_name']}")
            args = (f"./build/cgp path ./data/{self.setting['input_file']} print-fitness true generations {self.setting['cgp_gen']} load-circuit \"{circuit}\"")
            output_filename = f"{output_dir}/{self.setting['output_file']}"
            output_file = open(output_filename, 'a')
            self.proc = subprocess.Popen(args, shell=True, stdout=output_file, stderr=output_file)

    
    def proc_finished(self):
        if self.proc.poll() != None:
            return True
        return False
    
    def poll(self):
        if self.proc_finished():
            self.stage += 1
            if self.stage == self.n_stages:
                self.finished = True
            else:
                self.start()

def main():
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    max_processes = 40
    run_settings = RunSettings('optimalization_config.json')
    processes = []
    has_more_settings = True
    while True:
        while len(processes) < max_processes and has_more_settings:
            setting = run_settings.get_next_setting()
            if setting is None:
                has_more_settings = False
                break
            process = Process(setting)
            process.start()
            processes.append(process)
        time.sleep(1)
        finished = []
        for process in processes:
            process.poll()
            if process.finished:
                finished.append(process)
                run_settings.finish_setting(process.setting)
        for process in finished:
            processes.remove(process)
        if not processes and not has_more_settings:
            print('All finished!')
            break

if __name__ == '__main__':
    main()