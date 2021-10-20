#!/usr/bin/env python3

import re

matches = set()

file = "tb_mesh.spice"
pattern = 'vpwr_clk_buf1_\d+'
pattern = "ff_\d+_\d+"
lines = None
with open(file, 'r') as f:
    lines = f.readlines()

for line in lines:
    words = line.split()
    for word in words:
        if re.search(pattern, word):
            matches.add(word)

for match in sorted(matches):
    print(match)

