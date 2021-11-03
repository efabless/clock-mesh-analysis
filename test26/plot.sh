#!/usr/bin/env bash
set -euo pipefail


#    -l               : Disable the legend. By default signals from 1st raw-file get a legend.
#        -L               : Disable the grid. By default grid is shown.
#	    -T <titleString> : default none
#	        -X <xAxisLabel>  : default none. Note the scale is always fixed from 1st raw-file.
#		    -Y <yAxisLabel>  : default none

set -f
netlist=tb_mesh.spice
pattern="ff_\d+_\d+"
pattern="^clk_\d+"
../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o png/clock.png $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v -l -W '0,3e-9' -T 'Clock vs Time' -X 'Time(seconds' -Y 'Voltage(V)'
pattern="^vpwr_R_\d+"
#../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o png/vpwr_R_.png $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v
../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o png/power.png $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v -W '0,1e-8' -l -T 'Power vs Time' -X 'Time(seconds)' -Y 'Voltage(V)'
pattern="^co_i_\d+_\d+"
#../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o png/co_i.png $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v
pattern="^co_i_\d+_\d+"
../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o png/mesh_clock.png $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v -W '0.1e-8,0.8e-8' -l -T 'Mesh clock vs time' -X 'Time(seconds)' -Y 'Voltage(V)' 
pattern="^ff_clk_\d+_\d+"
../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o png/flipflop_clock.png $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v -W '0.1e-8,0.6e-8' -l -T 'Flipflop clock input vs Time' -X 'Time(seconds)' -Y 'Voltage(V)'
pattern="^ff_opt_clk_\d+_\d+"
../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o png/flipflop_opt_clock.png $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v -W '0.1e-8,0.6e-8' -l -T 'Opt-flipflop clock input vs Time' -X 'Time(seconds)' -Y 'Voltage(V)'
#../utils/rawn-plot1.py -g mesh_saveall/*/*1.8.raw -o png/ff_opt_clk_.png $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v -l
pattern="^ff_clk_static_\d+"
../utils/rawn-plot1.py -g mesh_saveall/*/*tt*1.8.raw -o png/direct_flipflop_tt.png $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v -W '0,0.8e-8' -l -s 'v(co_i_0_0)' -s 'v(co_i_1_0)' -s 'v(co_i_2_0)' -s 'v(co_i_3_0)' -s 'v(co_i_4_0)' -s 'v(co_i_5_0)' -T 'Direct flipflop vs Time(tt corner)' -X 'Time(seconds)' -Y 'Voltage(V)'
../utils/rawn-plot1.py -g mesh_saveall/*/*ss*1.8.raw -o png/direct_flipflop_ss.png $(../utils/get_signals.py $pattern $netlist | ../utils/list_to_args.py) -v -W '0,0.8e-8' -l -s 'v(co_i_0_0)' -s 'v(co_i_1_0)' -s 'v(co_i_2_0)' -s 'v(co_i_3_0)' -s 'v(co_i_4_0)' -s 'v(co_i_5_0)' -T 'Direct flipflop vs Time(ss corner)' -X 'Time(seconds)' -Y 'Voltage(V)'

