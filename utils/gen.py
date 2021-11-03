#!/usr/bin/env python3
import os
import sys
import textwrap
from random import uniform


def print_array(array):
    for item in array:
        print(item)


# a power network model as follows:
# met5 rails -> met4 stripes and -> vias and met1 rails decaped -> load buffers
def gen_power_network(power_source, prefix, branch_count, load_count, decaps_count):
    resistors = []
    decaps = []
    for i in list(range(branch_count)):
        branch = f"vpwr_{prefix}_branch_{i:<3}"
        R = f"RP_{prefix}_{i} {power_source} {branch} ${{R_{prefix}_BASE}}"
        resistors.append(R)

    for i in list(range(load_count)):
        branch_index = (i % branches)
        branch = f"vpwr_{prefix}_branch_{branch_index}"
        output = f"vpwr_{prefix}_{i}"
        load_resistor = f"RP_{prefix}_LOAD_{i:<2}"
        R = f"{load_resistor:<2} {branch:<2} {output:<2} ${{R_{prefix}_BUFF}}"
        resistors.append(R)

        for j in list(range(decaps_count)):
            decap = f"XDC_{prefix}_{j}_{i} VGND VNB {output} {output} sky130_fd_sc_hd__decap_12"
            decaps.append(decap)

    return resistors + decaps

# read the count of the single and double buffered flipflops

script_path = os.path.dirname(os.path.realpath(__file__))
buf16_file = os.path.join(script_path, "buf16.txt")
ff_file = os.path.join(script_path, "dfxtp2.txt")
buf16_opt_file = os.path.join(script_path, "buf16_opt.txt")
ff_opt_file = os.path.join(script_path, "dfxtp2_opt.txt")

with open(buf16_file) as reader:
    lines = reader.readlines()
buf16_count = list(map(int, lines))

with open(ff_file) as f:
    lines = f.readlines()
ff_per_buf16_count = [list(map(int, list(line.split()))) for line in lines]

with open(buf16_opt_file) as reader:
    lines = reader.readlines()
buf16_opt_count = list(map(int, lines))

with open(ff_opt_file) as f:
    lines = f.readlines()
ff_per_buf16_opt_count = [list(map(int, list(line.split()))) for line in lines]

netlist = []
pulses = []
buf16 = []
buf1 = []
co_resistor = []
buf16_ff = []
diodes_buf = []
buf1_16_intcon = []


decaps_count = 3
branches = 7
max_skew = 1.5

clock_buffer_per_source = 16
clock_source_count = 32
clock_buffer_load_flipflop = 10

ff_output_ports_index = 0
power_index = 0
ff_index = 0

power_network = gen_power_network(
    power_source="vpwr_0",
    prefix="R",
    branch_count=branches,
    load_count=clock_source_count * clock_buffer_per_source + clock_source_count,
    decaps_count=decaps_count
)

ff_clk_pin_cap = 0.00178
diode_pin_cap = 0.000878
load_cap = ff_clk_pin_cap + diode_pin_cap

# first group
for i in list(range(clock_source_count)):
    # randomly generated pulses from 0 to max_skew
    skew = str(round(uniform(0, max_skew), 2))
    pulse = f"0 1.8 {skew:>4}n 1n 1n 48n 100n"
    pulses.append(f"VC_{i:<2} clk_{i:<2} VGND pulse {pulse}")

    # pulses are output of clkbuf_1
    buffer = f"x1_{i:<2} clk_{i:<2} VGND VNB vpwr_R_{power_index:<2} vpwr_R_{power_index:<2} co_{i:<2} sky130_fd_sc_hd__clkbuf_1"
    power_index += 1
    buf1.append(buffer)

    # clkbuf_1 are shorted creating a mesh
    resistor = f"R_{i:<2} co_{i:<2} co_{i+1:<2} ${{R_LOAD}}"
    co_resistor.append(resistor)

    for j in list(range(buf16_count[i])):
        # .subckt int_con IN OUT GND C=2F R=30
        # interconnect between clkbuf_1 and clkbuf_16
        int_con = f"x_buf1_buf16_intcon_{i}_{j:<2} co_{i} co_i_{i}_{j:<2} VGND int_con C=8F R=120"
        buf1_16_intcon.append(int_con)

        # clkbuf_16 load on each clkbuf_1 based on buf16.txt
        buffer = f"x16_{i}_{j:<2} co_i_{i}_{j:<2} VGND VNB vpwr_R_{power_index:<2} vpwr_R_{power_index:<2} ff_{i}_{j:<2} sky130_fd_sc_hd__clkbuf_16"
        power_index += 1
        buf16.append(buffer)

        # diode capacitance model on each buf16 input
        diode = f"C_{i}_{j} co_i_{i}_{j:<2} VGND 0.9F"
        diodes_buf.append(diode)

        # flipflop(model) load on each buf16  based on dfxtp2.txt
        flipflop = f"xf_{i}_{j:<2} ff_{i}_{j:<2} ff_clk_{i}_{j:<2} VGND ff_rc m={ff_per_buf16_count[i][j]}"
        buf16_ff.append(flipflop)

opt_interconnect = []
buf16_opt_0 = []
diodes_opt = []
buf16_opt_1 = []
ff_opt = []

# second group
for i in list(range(len(buf16_opt_count))):
    for j in list(range(buf16_opt_count[i])):
        # interconnect between clkbuf_1 and clkbuf_16
        interconnect = f"x_buf16_opt_intcon_{i}_{j:<2} co_{i} co_i_opt_{i}_{j:<2} VGND int_con C=8F R=120"
        # first clkbuf_16
        buf16_0 = f"x_opt_0_{i}_{j:<2} co_i_opt_{i}_{j:<2} VGND VNB vpwr_R_{power_index:<2} vpwr_R_{power_index:<2} co_opt_0_{i}_{j:<2} sky130_fd_sc_hd__clkbuf_16"
        power_index += 1
        # second clkbuf_16
        buf16_1 = f"x_opt_1_{i}_{j:<2} co_opt_0_{i}_{j:<2} VGND VNB vpwr_R_{power_index:<2} vpwr_R_{power_index:<2} co_opt_1_{i}_{j:<2} sky130_fd_sc_hd__clkbuf_16"
        power_index += 1

        # flipflop(model) load on ech buf16 based on dfxtp2_opt.txt
        flipflop = f"xf_opt_{i}_{j:<2} co_opt_1_{i}_{j:<2} ff_opt_clk_{i}_{j:<2} VGND ff_rc m={ff_per_buf16_opt_count[i][j]}"

        # diode model on first clkbuf_16
        diode_0 = f"C_opt_0_{i}_{j:<2} co_i_opt_{i}_{j:<2} VGND 0.9F"
        # diode model on second clkbuf_16
        diode_1 = f"C_opt_1_{i}_{j:<2} co_opt_0_{i}_{j:<2} VGND 0.9F"

        ff_opt.append(flipflop)
        opt_interconnect.append(interconnect)
        buf16_opt_0.append(buf16_0)
        buf16_opt_1.append(buf16_1)
        diodes_opt.append(diode_0)
        diodes_opt.append(diode_1)

print(textwrap.dedent("""
    VVDD      vpwr_0 0  ${VDDD}
    VNB       VNB  0  0
    VVGND     VGND 0  0
    """))

# xf_opt_0_0  co_opt_1_0_0  ff_opt_clk_0_0  VGND ff_rc m=10

#    .CLK(clknet_5_0_1_core_clk),
#    .CLK(clknet_5_0_1_core_clk),
#    .CLK(clknet_5_8_1_core_clk),
#    .CLK(clknet_5_9_1_core_clk),
#    .CLK(clknet_5_22_1_core_clk),
#    .CLK(clknet_5_27_1_core_clk),
#    .CLK(clknet_5_30_1_core_clk),
#  x_buf1_buf16_intcon_0_0  co_0 co_i_0_0  VGND int_con C=8F R=120

netlist.append(power_network)
netlist.append(pulses)
netlist.append(buf1)
netlist.append(co_resistor)
netlist.append(buf1_16_intcon)
netlist.append(buf16)
netlist.append(buf16_ff)
netlist.append(diodes_buf)

netlist.append(opt_interconnect)
netlist.append(buf16_opt_0)
netlist.append(buf16_opt_1)
netlist.append(ff_opt)
netlist.append(diodes_opt)

for component in netlist:
    print_array(component)
    print('')

# third group
print(textwrap.dedent("""
    x_ff_static_0 co_i_0_0 ff_clk_static_0 VGND ff_rc
    x_ff_static_1 co_i_0_1 ff_clk_static_1 VGND ff_rc
    x_ff_static_2 co_i_1_0 ff_clk_static_2 VGND ff_rc
    x_ff_static_3 co_i_2_0 ff_clk_static_3 VGND ff_rc
    x_ff_static_4 co_i_3_0 ff_clk_static_4 VGND ff_rc
    x_ff_static_5 co_i_4_0 ff_clk_static_5 VGND ff_rc
    x_ff_static_6 co_i_5_0 ff_clk_static_6 VGND ff_rc
    """))

print(textwrap.dedent("""
    .lib     ../../../pdks/sky130A-1.0.227.01/libs.tech/ngspice/sky130.lib.spice ${CORNER}
    .include ../../../pdks/sky130A-1.0.227.01/libs.ref/sky130_fd_sc_hd/spice/sky130_fd_sc_hd.spice
    .include ../../subckts.spice

    .temp ${TEMP}
    .save all
    .tran 0.1n 50n

    .end"""))
