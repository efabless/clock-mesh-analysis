#!/bin/bash
rund=$(readlink -f $(dirname $0))
runn=$(basename $rund)
src=mesh32.spice
srcp=$rund/$src
logp=$rund/run.log

# rawFile="out.raw"
rawFile="RO:50_RB:20_RBUF:20.raw"

\cp -f ../../.spiceinit .

echo log: $logp
echo src: $srcp
echo in dir: $rund
echo
cd           $rund
echo running " ngspice -b $src -r $rawFile >& $logp"
exec ngspice -b $src -r $rawFile  >& $logp
# 
