#!/usr/bin/env python3

import fileinput

# Changes a list to args for rawn-plot1.py
# Usage: echo "signal" | python3 list_to_args.py
# Example: python3 get_signals.py 'ff_\d+_\d+' tb_mesh.spice | python3 list_to_args.py
arg = ""
for line in fileinput.input():
    signal = line.rstrip('\n')
    arg += f"-s v({signal}) "

print(arg)
