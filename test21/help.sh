#!/usr/bin/env bash
set -euo pipefail

pattern="ff_\d+_\d+"
pattern="^clk_\d+"
command="../utils/rawn-plot1.py $(../utils/get_signals.py $pattern tb_mesh.spice | ../utils/list_to_args.py)"
echo $command
