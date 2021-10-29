#!/bin/bash
rund=$(readlink -f $(dirname $0))
runn=$(basename $rund)
src=mesh.spice
srcp=$rund/$src
logp=$rund/run.log

echo log: $logp
echo src: $srcp
echo in dir: $rund
echo
#echo running: "simcorners tb.spi ${PDKPATH2} </dev/null >& $logp" ...
cd           $rund
echo running " ngspice -b $src -r output.raw >& $logp"
exec ngspice -b $src -r output.raw >& $logp
# 
