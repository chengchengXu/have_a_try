# coding: utf-8

import os
import json

for f in os.listdir():
    if not os.path.isfile(f):
        continue

    origin_file = f
    with open(origin_file, mode='r', encoding='utf-8') as f:
        content = f.read()

    x = eval(content)
    xs = [kv['source'] for kv in x if kv['cell_type']=='markdown']
    xs_c = sum(xs, [])

    real_str = ''.join(xs_c)

    new_file = origin_file.split('.')[0] + '.md'
    with open(new_file, mode='w', encoding='utf-8') as f:
        f.write(real_str)