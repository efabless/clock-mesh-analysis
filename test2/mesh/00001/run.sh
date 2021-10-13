#!/bin/bash
rund=$(readlink -f $(dirname $0))
runn=$(basename $rund)
src=mesh32.spice
srcp=$rund/$src
logp=$rund/run.log

# rawFile="out.raw"
rawFile="RO:20_RB:10_RBUF:30.raw"

\cp -f ../../.spiceinit .

echo log: $logp
echo src: $srcp
echo in dir: $rund
echo
cd           $rund
echo running " ngspice -b $src -r $rawFile >& $logp"
exec ngspice -b $src -r $rawFile  >& $logp
# 
