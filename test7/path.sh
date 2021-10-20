#!/usr/bin/env bash
set -euxo pipefail

../utils/rawn-plot1.py -o pdf/path.pdf -g 'mesh_saveall/*/*1.8.raw' -s 'v(vpwr_clk_buf1_1)' -s 'v(clk_1)' -s 'v(co_1)' -s 'v(co_i_1_0)' -s 'v(ff_1_0)' -s 'v(ff_clk_1_0)' -s 'v(vpwr_clk_buf1_branch_0)'
