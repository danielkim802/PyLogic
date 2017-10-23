from gate_components import *
from data_components import *
from arithmetic_components import *
from other_components import *

# rising clock edge detector
RisingClockEdgeDetector_w0 = Wire(1, 0)
RisingClockEdgeDetector_w1 = Wire(1)
RisingClockEdgeDetector_w2 = Wire(1)

RisingClockEdgeDetector_n0 = Not(1)
RisingClockEdgeDetector_a0 = And(2, 1)

RisingClockEdgeDetector_n0[0] = RisingClockEdgeDetector_w0
RisingClockEdgeDetector_n0["out"] = RisingClockEdgeDetector_w1
RisingClockEdgeDetector_a0[0] = RisingClockEdgeDetector_w1
RisingClockEdgeDetector_a0[1] = RisingClockEdgeDetector_w0
RisingClockEdgeDetector_a0["out"] = RisingClockEdgeDetector_w2

RisingClockEdgeDetector = Module({
	"in" : 1
},{
	"out" : 1
})

RisingClockEdgeDetector.add_component(RisingClockEdgeDetector_n0)
RisingClockEdgeDetector.add_component(RisingClockEdgeDetector_a0)
RisingClockEdgeDetector.assign_input("in", RisingClockEdgeDetector_n0, 0)
RisingClockEdgeDetector.assign_output("out", RisingClockEdgeDetector_a0, "out")

# 1 bit fulladder
FullAdder_A = Wire(1, 1)
FullAdder_B = Wire(1, 0)
FullAdder_Ci = Wire(1, 1)
FullAdder_w0 = Wire(1)
FullAdder_w2 = Wire(1)
FullAdder_w3 = Wire(1)
FullAdder_S = Wire(1)
FullAdder_Co = Wire(1)

FullAdder_x0 = Xor(2, 1)
FullAdder_x1 = Xor(2, 1)
FullAdder_a0 = And(2, 1)
FullAdder_a1 = And(2, 1)
FullAdder_o0 = Or(2, 1)

FullAdder_x0[0] = FullAdder_A
FullAdder_x0[1] = FullAdder_B
FullAdder_x0["out"] = FullAdder_w0
FullAdder_x1[0] = FullAdder_w0
FullAdder_x1[1] = FullAdder_Ci
FullAdder_x1["out"] = FullAdder_S
FullAdder_a0[0] = FullAdder_Ci
FullAdder_a0[1] = FullAdder_w0
FullAdder_a0["out"] = FullAdder_w2
FullAdder_a1[0] = FullAdder_B
FullAdder_a1[1] = FullAdder_A
FullAdder_a1["out"] = FullAdder_w3
FullAdder_o0[0] = FullAdder_w2
FullAdder_o0[1] = FullAdder_w3
FullAdder_o0["out"] = FullAdder_Co

FullAdder = Module({
	"A" : 1,
	"B" : 1,
	"Ci" : 1
},
{
	"S" : 1,
	"Co" : 1
})

for c in [FullAdder_x0, FullAdder_x1, FullAdder_a0, FullAdder_a1, FullAdder_o0]:
	FullAdder.add_component(c)

FullAdder.assign_input("A", FullAdder_x0, 0)
FullAdder.assign_input("B", FullAdder_x0, 1)
FullAdder.assign_input("Ci", FullAdder_x1, 1)
FullAdder.assign_output("S", FullAdder_x1, "out")
FullAdder.assign_output("Co", FullAdder_o0, "out")

# 32-bit counter
Counter32Bit_w0 = Wire(32)
Counter32Bit_w1 = Wire(32)
Counter32Bit_w2 = Wire(32)
Counter32Bit_adder = Adder(32)
Counter32Bit_reg = Register32Bit()
Counter32Bit_mux = Mux(2, 32)

Counter32Bit_adder["A"] = Wire(32, 1)
Counter32Bit_adder["B"] = Counter32Bit_w1
Counter32Bit_adder["Ci"] = Wire(1, 0)
Counter32Bit_adder["S"] = Counter32Bit_w0
Counter32Bit_adder["Co"] = Wire(1)
Counter32Bit_mux[0] = Counter32Bit_w0
Counter32Bit_mux[1] = Wire(32, 0)
Counter32Bit_mux["sel"] = Wire(1, 1)
Counter32Bit_mux["out"] = Counter32Bit_w2
Counter32Bit_reg["enable"] = Wire(1, 1)
Counter32Bit_reg["data"] = Counter32Bit_w2
Counter32Bit_reg["clk"] = Wire(1, 0)
Counter32Bit_reg["out"] = Counter32Bit_w1

Counter32Bit = Module({
	"enable" : 1,
	"clk" : 1
},{
	"count" : 32
})

Counter32Bit.add_component(Counter32Bit_adder)
Counter32Bit.add_component(Counter32Bit_reg)
Counter32Bit.add_component(Counter32Bit_mux)

Counter32Bit.assign_input("enable", Counter32Bit_reg, "enable")
Counter32Bit.assign_input("clk", Counter32Bit_reg, "clk")
Counter32Bit.assign_output("count", Counter32Bit_reg, "out")