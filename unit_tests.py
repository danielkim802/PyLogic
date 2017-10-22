from module_lib import *
from other_components import *
from arithmetic_components import *

# fulladder
for i in range(10):
	FullAdder.update_state()
	FullAdder.update()
	print FullAdder["A"].get_value()
	print FullAdder["B"].get_value()
	print FullAdder["Ci"].get_value()
	print FullAdder["S"].get_value()
	print FullAdder["Co"].get_value()
	print

# rising clock edge detector
for i in range(10):
	if i == 5:
		RisingClockEdgeDetector["in"].set_value(1)

	RisingClockEdgeDetector.update_state()
	RisingClockEdgeDetector.update()

	print RisingClockEdgeDetector["in"].get_value()
	print RisingClockEdgeDetector["out"].get_value()
	print

# 2bit mux
mux = Mux(2, 8)
mux[0] = Wire(8, 0xff)
mux[1] = Wire(8, 0xee)
mux["sel"] = Wire(1, 0)
mux["out"] = Wire(8)

mux.update_state()
mux.update()

print mux.input_state
print mux.output_state
print mux["out"].get_value()

# adder 
adder = Adder(8)
adder["A"] = Wire(8, 0x11)
adder["B"] = Wire(8, 0x22)
adder["Ci"] = Wire(1, 1)
adder["Co"] = Wire(1)
adder["S"] = Wire(8)

adder.update_state()
adder.update()

print adder["S"].get_value()
print 0x34