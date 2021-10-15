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
_EOF
} | xargs -n 1 -P 60 /bin/bash
