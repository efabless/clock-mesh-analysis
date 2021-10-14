#!/bin/bash
rund=$(readlink -f $(dirname $0))
runn=$(basename $rund)
src=mesh32.spice
srcp=$rund/$src
logp=$rund/run.log

# rawFile="out.raw"
rawFile="RO:${RLOAD}_RB:${R_BASE}_RBUF:${R_BUFF}.raw"

echo log: $logp
echo src: $srcp
echo in dir: $rund
echo
cd $rund
echo "set ngbehavior=hsa" > .spiceinit
echo running " ngspice -b $src -r $rawFile >& $logp"
exec ngspice -b $src -r $rawFile  >& $logp
# 
