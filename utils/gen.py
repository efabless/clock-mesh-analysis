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
        load_resistor = f"RP_{prefix}_LOAD_{i}"
        R = f"{load_resistor:20} {branch:23} {output:23} ${{R_{prefix}_BUFF}}"
        resistors.append(R)

        for j in list(range(decaps_count)):
            decap = f"XDC_{prefix}_{j}_{i} VGND VNB {output} {output} sky130_fd_sc_hd__decap_12"
            decaps.append(decap)

    return resistors + decaps


netlist = []
pulses = []
buffers = []
load_resistors = []
leafs = []
load_flipflops = []
load_caps = []

decaps_count = 3
branches = 7
buffers_count = 32
max_skew = 2
ff_output_ports_count = 10

ff_output_ports_index = 0

power_network = gen_power_network(
    power_source="vpwr_0",
    prefix="clk_buf1",
    branch_count=branches,
    load_count=buffers_count,
    decaps_count=decaps_count
)

netlist.append(power_network)

for i in list(range(buffers_count)):
    # random clock pulse between 0 and max_skew value
    skew = str(round(uniform(0, max_skew), 2))
    pulse = f"0 1.8 {skew:>4}n 1n 1n 48n 100n"
    pulses.append(f"VC_{i:<2} clk_{i:<2} VGND pulse {pulse}")

    # buffers directly connected to clock sources
    buffer = f"x0_{i:<2} clk_{i:<2} VGND VNB vpwr_clk_buf1_{i:<2} vpwr_clk_buf1_{i:<2} co_{i:<2} sky130_fd_sc_hd__clkbuf_1"
    buffers.append(buffer)

    # (load) clock buffers connected to the mesh at different points
    leaf = f"x1_{i:<2} co_{i:<2} VGND VNB vpwr_clk_buf1_{i:<2} vpwr_clk_buf1_{i:<2} ff_{i:<2} sky130_fd_sc_hd__clkbuf_16"
    leafs.append(leaf)

    # load resistors between shorted net (mesh)
    resistor = f"R_{i:<2} co_{i:<2} co_{i+1:<2} ${{RLOAD}}"
    load_resistors.append(resistor)

    # load capacitance
    load_cap = f"Cp_{i:<2} co_{i:<2} VGND ${{CP_LOAD}}"
    load_caps.append(load_cap)

    # each load buffer is connected to multiple flipflops
    ff_output_ports = ""
    for x in list(range(ff_output_ports_count)):
        ff_output_ports_index = int(ff_output_ports_index) + int(1)
        ff_output_ports += f"Q{ff_output_ports_index:<3} "
    
    load_flipflop = f"X10F_{i:<2} vpwr_0 VGND ff_{i:<2} {ff_output_ports} DFXTP_2_10X"
    load_flipflops.append(load_flipflop)


print(textwrap.dedent("""
    VVDD      vpwr_0 0  ${VDDD}
    VNB       VNB  0  0
    VVGND     VGND 0  0
    """))

netlist.append(pulses)
netlist.append(buffers)
netlist.append(load_resistors)
netlist.append(leafs)
netlist.append(load_flipflops)
for component in netlist:
    print_array(component)
    print('')

print(textwrap.dedent("""
    .lib     ../../../pdks/sky130A-1.0.227.01/libs.tech/ngspice/sky130.lib.spice ${CORNER}
    .include ../../../pdks/sky130A-1.0.227.01/libs.ref/sky130_fd_sc_hd/spice/sky130_fd_sc_hd.spice
    .include ../../dfxtp_2_10x.spice

    .temp ${TEMP}
    .save all
    .tran 0.1n 100n

    .end"""))
