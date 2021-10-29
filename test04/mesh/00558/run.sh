#!/bin/bash
rund=$(readlink -f $(dirname $0))
runn=$(basename $rund)
src=mesh32.spice-b
srcp=$rund/$src
logp=$rund/run.log

# rawFile="out.raw"
rawFile="CORNER:ff_RO:70_RB:10_RBUF:50_TEMP:-40_VDD:1.6.raw"

echo log: $logp
echo src: $srcp
echo in dir: $rund
echo
cd $rund
echo "set ngbehavior=hsa" > .spiceinit
echo running " ngspice -b $src -r $rawFile >& $logp"
exec ngspice -b $src -r $rawFile  >& $logp
# 
