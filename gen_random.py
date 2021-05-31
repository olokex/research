import random
import os

N_FUNCS = 1000
N_INPUTS = 6
N_OUTPUTS = 1

generated = set()

if not os.path.exists('funcs'):
	os.makedirs('funcs')

n = 0
while n < N_FUNCS:
	s = ''
	for i in range(0, 2**N_INPUTS):
		s += f'{bin(i)[2:].zfill(N_INPUTS)} {"".join(random.choice("01") for j in range(N_OUTPUTS))}\n'
	if s in generated:
		continue
	generated.add(s)
	with open(f'funcs/func{str(n).zfill(len(str(N_FUNCS - 1)))}', 'w') as f:
		f.write(s)
	n += 1