#!/usr/bin/env python3

import sys
import re

matches = set()

#pattern = 'vpwr_clk_buf1_\d+'
#pattern = "ff_\d+_\d+"
file = sys.argv[2]
pattern = sys.argv[1]
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

