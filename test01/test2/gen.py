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


<<<<<<< HEAD
print(
    """
VVDD      vpwr0 0  1.8
VNB       VNB  0  0
VVGND     VGND 0  0
""")

iterations = 32
for i in list(range(iterations)):
    skew = str(round(uniform(0, 1), 2))
    pulse = f"0 1.8 {skew}n 1n 1n 48n 100n"
    pulses.append(f"VC{i} clk{i} VGND pulse {pulse}")

    buffer = f"x0{i} clk{i} VGND VNB vpwr{i+1} vpwr{i+1} co{i} sky130_fd_sc_hd__clkbuf_1"
    #buffer = f"x0{i} clk{i} VGND VNB vpwr0 vpwr0 co{i} sky130_fd_sc_hd__clkbuf_1"
    buffers.append(buffer)

    resistor = f"R{i} co{i} co{i+1} 10"
    resistors.append(resistor)

    leaf = f"x1{i} co{i+1} VGND VNB vpwr0 vpwr0 ff{i} sky130_fd_sc_hd__clkbuf_16"
    leafs.append(leaf)

    power_resistor = f"RP{i} vpwr{i} vpwr{i+1} 10"
    power_resistors.append(power_resistor)

#XDC1 VGND VNB vpwr1 vpwr1 sky130_fd_sc_hd__decap_12 
    power_cap = f"XDC{i}_{i} VGND VNB vpwr{i+1} vpwr{i+1} sky130_fd_sc_hd__decap_12"
    power_caps.append(power_cap)
    power_cap = f"XDC{i}_{i}_{i} VGND VNB vpwr{i+1} vpwr{i+1} sky130_fd_sc_hd__decap_12"
    power_caps.append(power_cap)
    power_cap = f"XDC{i}_{i}_{i}_{i} VGND VNB vpwr{i+1} vpwr{i+1} sky130_fd_sc_hd__decap_12"
    power_caps.append(power_cap)
    power_cap = f"XDC{i}_{i}_{i}_{i}_{i} VGND VNB vpwr{i+1} vpwr{i+1} sky130_fd_sc_hd__decap_12"
    power_caps.append(power_cap)

print_array(pulses)
print('')
=======
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
>>>>>>> dbc46f348ae7a816e2c36737b81e976167234d41
print_array(buffers)
print('')
print_array(resistors)
print('')
print_array(leafs)
print('')
<<<<<<< HEAD
print_array(power_resistors)
print('')
=======
>>>>>>> dbc46f348ae7a816e2c36737b81e976167234d41
print_array(power_caps)

print(
    """
.lib /ciic/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice tt
.include /ciic/pdks/sky130A/libs.ref/sky130_fd_sc_hd/spice/sky130_fd_sc_hd.spice
""")
<<<<<<< HEAD

for i in list(range(iterations)):
    print(f".save clk{i}")
print('')
for i in list(range(iterations + 1)):
    print(f".save co{i}")
print('')
for i in list(range(iterations)):
    print(f".save ff{i}")
print('')
for i in list(range(iterations)):
    print(f".save vpwr{i}")
print('')
=======
# print("""
# .GLOBAL GND
# .GLOBAL VNB
# .GLOBAL VGND
# .GLOBAL VPWR
# .GLOBAL VPB
# """)
>>>>>>> dbc46f348ae7a816e2c36737b81e976167234d41


print(
    """
<<<<<<< HEAD
=======
.save all
>>>>>>> dbc46f348ae7a816e2c36737b81e976167234d41
.options savecurrents
.tran 2n 250n

.end"""
)
