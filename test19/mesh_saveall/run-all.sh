#!/bin/bash
rund=$(readlink -f $(dirname $0))
logp=$rund/run-all.log

echo log: $logp
echo in dir: $rund
echo
cd           $rund
exec </dev/null >& $logp
{ cat <<_EOF
./00000/run.sh
./00001/run.sh
./00002/run.sh
_EOF
} | xargs -n 1 -P 32 /bin/bash
