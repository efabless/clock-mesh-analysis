#!/usr/bin/env bash
set -euo pipefail

set -f
netlist=tb_mesh.spice
pattern="ff_\d+_\d+"
pattern="^clk_\d+"
../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o pdf/clk_.pdf $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v
pattern="^vpwr_R_\d+"
../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o pdf/vpwr_R_.pdf $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v
../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o pdf/vpwr_R_zoom_.pdf $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v -W '0,1e-8'
pattern="^co_i_\d+_\d+"
../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o pdf/co_i.pdf $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v
pattern="^co_i_\d+_\d+"
../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o pdf/co_i_zoom.pdf $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v -W '0,0.8e-8' -l
pattern="^ff_clk_\d+_\d+"
../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o pdf/ff_clk_zoom.pdf $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v -W '0,0.6e-8' -l
pattern="^ff_opt_clk_\d+_\d+"
../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o pdf/ff_opt_clk_zoom.pdf $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v -W '0,0.6e-8' -l
../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o pdf/ff_opt_clk_.pdf $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v -l
pattern="^ff_clk_static_\d+"
../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o pdf/ff_clk_static_zoom.pdf $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v -W '0,0.8e-8' -l

