#!/usr/bin/env bash
set -euxo pipefail

index=1
../utils/rawn-plot1.py -o pdf/path_$index.pdf -g 'mesh_saveall/*/*1.8.raw' -s "v(vpwr_clk_buf1_$index)" -s "v(clk_$index)" -s "v(co_$index)" -s "v(co_i_${index}_0)" -s "v(ff_${index}_0)" -s "v(ff_clk_${index}_0)" -s 'v(vpwr_clk_buf1_branch_0)'
