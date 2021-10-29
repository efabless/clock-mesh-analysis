#!/usr/bin/env python3

import fileinput

arg = ""
for line in fileinput.input():
    signal = line.rstrip('\n')
    arg += f"-s v({signal}) "

print(arg)
