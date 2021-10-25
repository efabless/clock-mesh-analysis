#!/bin/bash
rund=$(readlink -f $(dirname $0))
runn=$(basename $rund)
src=mesh.spice
srcp=$rund/$src
logp=$rund/run.log

# rawFile="out.raw"
rawFile="CORNER:ss_RO:${RLOAD}_RB:${R_BASE}_RBUF:${R_BUFF}_TEMP:25_VDD:1.8.raw"

echo log: $logp
echo src: $srcp
echo in dir: $rund
echo
cd $rund
echo "set ngbehavior=hsa" > .spiceinit
echo running " ngspice -b $src -r $rawFile >& $logp"
exec ngspice -b $src -r $rawFile  >& $logp
# 
