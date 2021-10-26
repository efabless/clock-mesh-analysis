#!/usr/bin/env bash
set -euo pipefail

nets=(
clknet_5_0_1_core_clk
clknet_5_1_1_core_clk
clknet_5_2_1_core_clk
clknet_5_3_1_core_clk
clknet_5_4_1_core_clk
clknet_5_5_1_core_clk
clknet_5_6_1_core_clk
clknet_5_7_1_core_clk
clknet_5_8_1_core_clk
clknet_5_9_1_core_clk
clknet_5_10_1_core_clk
clknet_5_11_1_core_clk
clknet_5_12_1_core_clk
clknet_5_13_1_core_clk
clknet_5_14_1_core_clk
clknet_5_15_1_core_clk
clknet_5_16_1_core_clk
clknet_5_17_1_core_clk
clknet_5_18_1_core_clk
clknet_5_19_1_core_clk
clknet_5_20_1_core_clk
clknet_5_21_1_core_clk
clknet_5_22_1_core_clk
clknet_5_23_1_core_clk
clknet_5_24_1_core_clk
clknet_5_25_1_core_clk
clknet_5_26_1_core_clk
clknet_5_27_1_core_clk
clknet_5_28_1_core_clk
clknet_5_29_1_core_clk
clknet_5_30_1_core_clk
clknet_5_31_1_core_clk
)

help() {
    arr=($(grep $1 ./mgmt_core.v -A 2 | grep "\.A" -A 1 | grep -P "clknet_leaf_\d*_core_clk" -o))
    for buf16_out in "${arr[@]}"; do
        count=$(grep $buf16_out mgmt_core.v -B 2 | grep "\.CLK" | wc -l)
        echo $'\t' $buf16_out ---- $count dfxtp2
        echo -n "$count " >> dfxtp2.txt
    done
}


for net in "${nets[@]}"; do
    leaf=$(help $net)
    echo "" >> dfxtp2.txt
    count=$(echo "$leaf" | wc -l)
    echo $count >> buf16.txt
    echo "### ${net} ---- ${count} buf16"
    echo ""
    echo "${leaf}"
    echo ""
done

