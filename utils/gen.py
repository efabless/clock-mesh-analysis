#!/usr/bin/env python3
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
        branch = f"vpwr_{prefix}_branch_{i}"
        R = f"RP_{prefix}_{i} {power_source} {branch:23} ${{R_{prefix}_BASE}}"
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


netlist = []
pulses = []
buf16 = []
buf1 = []
co_resistor = []
leafs = []
buf16_ff = []
load_caps = []
diodes_buf = []
diodes_ff = []


decaps_count = 3
branches = 7
buffers_count = 32
buffer_fanout = 15
max_skew = 2
ff_output_ports_count = 10

clock_source_count = 32
clock_buffer_per_source = 2
clock_buffer_load_flipflop = 2

ff_output_ports_index = 0
power_index = 0
ff_index = 0

power_network = gen_power_network(
    power_source="vpwr_0",
    prefix="clk_buf1",
    branch_count=branches,
    load_count=clock_source_count,
    decaps_count=decaps_count
)


for i in list(range(clock_source_count)):
    skew = str(round(uniform(0, max_skew), 2))
    pulse = f"0 1.8 {skew:>4}n 1n 1n 48n 100n"
    pulses.append(f"VC_{i:<2} clk_{i:<2} VGND pulse {pulse}")

    buffer = f"x1_{i:<2} clk_{i:<2} VGND VNB vpwr_clk_buf1_{i:<2} vpwr_clk_buf1_{i:<2} co_{i:<2} sky130_fd_sc_hd__clkbuf_1"
    buf1.append(buffer)

    resistor = f"R_{i:<2} co_{i:<2} co_{i+1:<2} ${{R_LOAD}}"
    co_resistor.append(resistor)

    for j in list(range(clock_buffer_per_source)):
        buffer = f"x16_{i}_{j:<2} co_{i:<2} VGND VNB vpwr_clk_buf1_{i:<2} vpwr_clk_buf1_{i:<2} ff_{i}_{j:<2} sky130_fd_sc_hd__clkbuf_16"
        buf16.append(buffer)

        diode = f"xdiode_{i}_{j:<2} co_{i:<2} VGND VNB vpwr_0 vpwr_0 sky130_fd_sc_hd__diode_2"
        diodes_buf.append(diode)

        for k in list(range(clock_buffer_load_flipflop)):
            flipflop = f"xf_{i}_{j}_{k:<2} ff_{i}_{j:<2} VGND VGDN VGND vpwr_0 vpwr_0 Q{ff_index} sky130_fd_sc_hd__dfxtp_2"
            buf16_ff.append(flipflop)
            ff_index += 1

            diode = f"xdiode_{i}_{j}_{k:<2} ff_{i}_{j:<2} VGND VNB vpwr_0 vpwr_0 sky130_fd_sc_hd__diode_2"
            diodes_ff.append(diode)


print(textwrap.dedent("""
    VVDD      vpwr_0 0  ${VDDD}
    VNB       VNB  0  0
    VVGND     VGND 0  0
    """))

netlist.append(power_network)
netlist.append(pulses)
netlist.append(co_resistor)
netlist.append(buf1)
netlist.append(buf16)
netlist.append(buf16_ff)
netlist.append(diodes_ff)
netlist.append(diodes_buf)
for component in netlist:
    print_array(component)
    print('')

print(textwrap.dedent("""
    .lib     ../../../pdks/sky130A-1.0.227.01/libs.tech/ngspice/sky130.lib.spice ${CORNER}
    .include ../../../pdks/sky130A-1.0.227.01/libs.ref/sky130_fd_sc_hd/spice/sky130_fd_sc_hd.spice

    .temp ${TEMP}
    .save all
    .tran 0.1n 100n

    .end"""))
