#!/usr/bin/env python3
import sys


def get_signal_args(prefix, type, count):
    args = ""
    for i in list(range(count)):
        arg = f"-s \'{type}({prefix}{i})\' "
        args += arg

    return args


plot_script = "./utils/rawn-plot1.py"
signal_type = sys.argv[1]
signal_prefix = sys.argv[2]
signal_count = int(sys.argv[3])
raw_files = ' '.join([str(elem) for elem in sys.argv[4:]])

signals_arg = get_signal_args(prefix=signal_prefix,
                              type=signal_type, count=signal_count)

command = f"{plot_script} -o {signal_prefix}.pdf {signals_arg} {raw_files}"
print(command)
