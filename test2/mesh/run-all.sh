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
./00003/run.sh
./00004/run.sh
./00005/run.sh
./00006/run.sh
./00007/run.sh
./00008/run.sh
./00009/run.sh
./00010/run.sh
./00011/run.sh
./00012/run.sh
./00013/run.sh
./00014/run.sh
./00015/run.sh
./00016/run.sh
./00017/run.sh
./00018/run.sh
./00019/run.sh
./00020/run.sh
./00021/run.sh
./00022/run.sh
./00023/run.sh
./00024/run.sh
./00025/run.sh
./00026/run.sh
_EOF
} | xargs -n 1 -P 60 /bin/bash
