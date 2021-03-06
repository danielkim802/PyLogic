from pylogic import *

# fulladder
FullAdder = FullAdder()
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
RisingClockEdgeDetector = RisingClockEdgeDetector()
for i in range(10):
	if i == 5:
		RisingClockEdgeDetector["in"].set_value(1)

	RisingClockEdgeDetector.update_state()
	RisingClockEdgeDetector.update()

	print RisingClockEdgeDetector["in"].get_value()
	print RisingClockEdgeDetector["out"].get_value()
	print

# 1bit mux
mux = Mux(2, 8)
mux[0] = Wire(8, 0xff)
mux[1] = Wire(8, 0xee)
mux["sel"] = Wire(1, 1)
mux["out"] = Wire(8)

mux.update_state()
mux.update()

print mux.input_state
print mux.output_state
print mux["out"].get_value()
print

# 2bit mux
mux = Mux(3, 2)
mux[0] = Wire(2, 0)
mux[1] = Wire(2, 0)
mux[2] = Wire(2, 1)
mux["sel"] = Wire(2, 2)
mux["out"] = Wire(2)

mux.update_state()
mux.update()

print mux.input_state
print mux.output_state
print mux["out"].get_value()
print

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
print 

# 32bit counter
counter = Counter32Bit()
circuit = Circuit()
circuit.add_component(counter)
circuit.set_clock_period(3)				# critical path is 3 components long
counter["clk"] = circuit.get_clk()
counter["count"] = Wire(32)
counter["enable"] = Wire(1, 1)
counter["reset"] = Wire(1, 0)
circuit.trace(counter, "count")
circuit.trace(counter, "enable")
circuit.trace(counter, "reset")
for i in range(100):
	if i == 51:
		counter["enable"].set_value(0)
	if i == 60:
		counter["reset"].set_value(1)
		counter["enable"].set_value(1)
	circuit.update()

# shifter
rshift = ShiftRightLogical(32, 1)
rshift["A"] = Wire(32, 0xdeadbeef)
rshift["shift"] = Wire(1, 1)
rshift["out"] = Wire(32)

rshift.update_state()
rshift.update()

print hex(rshift["out"].get_value())

# wire tests
w0 = Wire(8, 0x13)
w1 = Wire(8, 0x25)
a = Wire(8)
a[7:4] = w0[3:0]
a[3:0] = w1[7:4]
b = Wire(4)
b[1:0] = a[1:0]
b[2] = Wire(1, 0)
b[3] = Wire(1, 1)

print bin(b.get_value())

w = Wire(16)
w[15:8] = w1[7:0]
w[7:0] = w0[7:0]

print hex(w.get_value())

a = Wire(8)
a[7:0] = w[11:4]
print hex(a.get_value())

w = Wire(8, 0x11)
a = And(2, 8)
o = Wire(8)
a[0] = w
a[1] = Wire(8)
a[1][3:0] = b = w0[7:4]
a[1][7:4] = c = w1[3:0]

a.update_state()
a.update()
a.update_state()
a.update()
a.update_state()
a.update()

print a['out'].get_value()

w0.set_value(0x11)

a.update_state()
a.update()
a.update_state()
a.update()
a.update_state()
a.update()

print a['out'].get_value()