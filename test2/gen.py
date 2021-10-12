#!/usr/bin/env python3
from random import seed, uniform

pulses = []
buffers = []
resistors = []
leafs = []
power_resistors = []
power_caps = []


def print_array(array):
    for item in array:
        print(item)


decaps_count = 3
branches = 7
buffers_count = 32
for i in list(range(branches)):
    power_resistors.append(
        f"RP_{i} vpwr_0 vpwr_branch_{i} ${{R_BASE}}"
    )


for i in list(range(buffers_count)):
    skew = str(round(uniform(1, 8), 2))
    pulse = f"0 1.8 {skew}n 1n 1n 48n 100n"
    pulses.append(f"VC_{i} clk_{i} VGND pulse {pulse}")

    branch = (i % branches)
    power_resistors.append(
        f"RP_BUFF_{i} vpwr_branch_{branch} vpwr_buff_{i} ${{R_BUFF}}"
    )

    buffer = f"x0_{i} clk_{i} VGND VNB vpwr_buff_{i} vpwr_buff_{i} co_{i} sky130_fd_sc_hd__clkbuf_1"
    #buffer = f"x0_{i} clk_{i} VGND VNB vpwr0 vpwr0 co_{i} sky130_fd_sc_hd__clkbuf_1"
    buffers.append(buffer)

    resistor = f"R_{i} co_{i} co_{i} ${{RLOAD}}"
    resistors.append(resistor)

    leaf = f"x1_{i} co_{i} VGND VNB vpwr_0 vpwr_0 ff_{i} sky130_fd_sc_hd__clkbuf_16"
    leafs.append(leaf)

    # power_resistor = f"RP_{i} vpwr_{i} vpwr_{i} ${{RPWR}}"
    # power_resistors.append(power_resistor)

    for j in list(range(decaps_count)):
        power_cap = f"XDC{j}_{i} VGND VNB vpwr_buff_{i} vpwr_buff_{i} sky130_fd_sc_hd__decap_12"
        power_caps.append(power_cap)


print(
    """
VVDD      vpwr_0 0  1.8
VNB       VNB  0  0
VVGND     VGND 0  0
    """)
print_array(pulses)
print('')
print_array(power_resistors)
print('')
print_array(buffers)
print('')
print_array(resistors)
print('')
print_array(leafs)
print('')
print_array(power_caps)

print(
    """
.lib /ciic/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice tt
.include /ciic/pdks/sky130A/libs.ref/sky130_fd_sc_hd/spice/sky130_fd_sc_hd.spice
""")
# print("""
# .GLOBAL GND
# .GLOBAL VNB
# .GLOBAL VGND
# .GLOBAL VPWR
# .GLOBAL VPB
# """)


print(
    """
.save all
.options savecurrents
.tran 2n 250n

.end"""
)
