#!/usr/bin/env bash

set -xu

dir=mesh
output_spice=mesh32.spice-b
run_template=run_template.sh
tb=mesh32.spice-b
cfg=mesh.cfg
../utils/enumer.py -v -d $dir -o $output_spice -r $run_template $tb $cfg
