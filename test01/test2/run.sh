#!/usr/bin/env bash

set -xu

dir=mesh
output_spice=mesh.spice
run_template=run_template.sh
tb=tb_mesh.spice
cfg=mesh.cfg
/ciic/tools/efabless/bin/enumer -v -d $dir -o $output_spice -r $run_template $tb $cfg