import sys
sys.path.insert(0, "../src")

from pylogic import *

def MultiplierControlFSM():
	# instantiate module
	MultiplierControlFSM = Module(
		{
			"lsb"      : 1,
			"req_val"  : 1,
			"resp_rdy" : 1,
			"clk"      : 1
		}, {
			"req_rdy"  : 1,
			"resp_val" : 1, 
			"b_sel"    : 1, 
			"a_sel"    : 1, 
			"add_sel"  : 1, 
			"r_sel"    : 1
		}
	)

	# initialize wires
	w0 = Wire(2)
	w1 = Wire(2)
	w2 = Wire(2)
	w3 = Wire(2)
	w4 = Wire(1)
	w5 = Wire(32)
	w6 = Wire(1)
	w7 = Wire(1)
	w8 = Wire(1)
	wstate = Wire(2)

	# initialize state register and counter
	state_reg = Register2Bit()
	counter = Counter32Bit()

	# initialize additional components
	mstate = Mux(3, 2)
	m0 = Mux(2, 2)
	m1 = Mux(2, 2)
	m2 = Mux(2, 2)
	m3 = Mux(3, 1)
	m4 = Mux(3, 1)
	m5 = Mux(3, 1)
	m6 = Mux(3, 1)
	m7 = Mux(3, 1)
	m8 = Mux(3, 1)
	m9 = Mux(3, 1)
	m10 = Mux(3, 1)
	comp = Comparator32Bit()
	n = Not(1)

	# connect everything together
	mstate["out"] = w2
	mstate[0] = w0
	mstate[1] = w1
	mstate[2] = w3
	mstate["sel"] = wstate

	m0["out"] = w0
	m0[0] = Wire(2, 0)
	m0[1] = Wire(2, 1)

	m1["out"] = w1
	m1[0] = Wire(2, 1)
	m1[1] = Wire(2, 2)
	m1["sel"] = w4

	m2["out"] = w3
	m2[0] = Wire(2, 2)
	m2[1] = Wire(2, 0)

	m3["out"] = w6
	m3[0] = Wire(1, 0)
	m3[1] = Wire(1, 1)
	m3[2] = Wire(1, 1)
	m3["sel"] = wstate

	m4[0] = Wire(1, 1)
	m4[1] = Wire(1, 0)
	m4[2] = Wire(1, 0)
	m4["sel"] = wstate

	m5[0] = Wire(1, 0)
	m5[1] = Wire(1, 0)
	m5[2] = Wire(1, 1)
	m5["sel"] = wstate

	m6[0] = Wire(1, 1)
	m6[1] = Wire(1, 0)
	m6[2] = Wire(1)
	m6["sel"] = wstate

	m7[0] = Wire(1, 1)
	m7[1] = Wire(1, 0)
	m7[2] = Wire(1)
	m7["sel"] = wstate

	m8[0] = Wire(1)
	m8[1] = w7
	m8[2] = Wire(1, 1)
	m8["sel"] = wstate

	m9[0] = Wire(1, 1)
	m9[1] = Wire(1, 0)
	m9[2] = Wire(1, 0)
	m9["sel"] = wstate

	m10[0] = Wire(1, 0)
	m10[1] = Wire(1, 0)
	m10[2] = Wire(1, 1)
	m10["sel"] = wstate
	m10["out"] = w8

	n["out"] = w7

	comp["out"] = w4
	comp["A"] = w5
	comp["B"] = Wire(32, 31)

	state_reg["data"] = w2
	state_reg["enable"] = Wire(1, 1)
	state_reg["out"] = wstate

	counter["count"] = w5
	counter["enable"] = w6
	counter["reset"] = w8

	state_reg["clk"] = counter["clk"] = Wire(1)
	
	# add components to module
	components = [state_reg, counter, mstate, m0, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, comp, n]
	for component in components:
		MultiplierControlFSM.add_component(component)
	
	# assign module inputs and outputs
	MultiplierControlFSM["lsb"] = n[0]
	MultiplierControlFSM["req_val"] = m0["sel"]
	MultiplierControlFSM["resp_rdy"] = m2["sel"]
	MultiplierControlFSM["clk"] = state_reg["clk"]
	MultiplierControlFSM["clk"] = counter["clk"]
	MultiplierControlFSM["req_rdy"] = m4["out"]
	MultiplierControlFSM["resp_val"] = m5["out"]
	MultiplierControlFSM["b_sel"] = m6["out"]
	MultiplierControlFSM["a_sel"] = m7["out"]
	MultiplierControlFSM["add_sel"] = m8["out"]
	MultiplierControlFSM["r_sel"] = m9["out"]

	return MultiplierControlFSM

def MultiplierDataPath():
	# instantiate module
	MultiplierDataPath = Module(
		{
			"req_msg"  : 64,
			"b_sel"    : 1,
			"a_sel"    : 1,
			"r_sel"    : 1,
			"add_sel"  : 1,
			"clk"      : 1
		}, {
			"lsb"      : 1,
			"resp_msg" : 32
		}
	)

	# initialize wires
	w1 = Wire(32)
	w2 = Wire(32)
	w3 = Wire(32)
	w4 = Wire(32)
	w5 = Wire(32)
	w6 = Wire(32)
	w7 = Wire(32)
	w8 = Wire(32)
	w9 = Wire(32)
	w10 = Wire(32)
	w11 = Wire(32)
	w12 = Wire(32)
	w13 = Wire(32)

	# initialize components
	bmux = Mux(2, 32)
	amux = Mux(2, 32)
	rmux = Mux(2, 32)
	addmux = Mux(2, 32)
	rshift = ShiftRightLogical(32, 1)
	lshift = ShiftLeftLogical(32, 1)
	breg = Register32Bit()
	areg = Register32Bit()
	rreg = Register32Bit()
	comp = Comparator32Bit()
	a = And(2, 32)
	split = Splitter64Bit()
	adder = Adder(32)

	# connect everything together
	bmux[0] = w1
	bmux[1] = w5
	bmux["out"] = w2

	amux[0] = w6
	amux[1] = w7
	amux["out"] = w8

	rmux[0] = w10
	rmux[1] = Wire(32, 0)
	rmux["out"] = w11

	addmux[0] = w13
	addmux[1] = w12
	addmux["out"] = w10

	rshift["A"] = w3
	rshift["shift"] = Wire(1, 1)
	rshift["out"] = w1

	lshift["A"] = w9
	lshift["shift"] = Wire(1, 1)
	lshift["out"] = w6

	breg["data"] = w2
	breg["enable"] = Wire(1, 1)
	breg["out"] = w3

	areg["data"] = w8
	areg["enable"] = Wire(1, 1)
	areg["out"] = w9

	rreg["data"] = w11
	rreg["enable"] = Wire(1, 1)
	rreg["out"] = w12

	comp["A"] = w4
	comp["B"] = Wire(32, 1)

	a[0] = w3
	a[1] = Wire(32, 1)
	a["out"] = w4

	split["lsb"] = w5
	split["msb"] = w7

	adder["A"] = w9
	adder["B"] = w12
	adder["Ci"] = Wire(1, 0)
	adder["S"] = w13

	breg["clk"] = areg["clk"] = rreg["clk"] = Wire(1)
	rreg["out"] = addmux[1] = adder["B"] = Wire(32)

	# add components to module
	components = [bmux, amux, rmux, addmux, rshift, lshift, breg, areg, rreg, comp, a, split, adder]
	for component in components:
		MultiplierDataPath.add_component(component)

	# assign module inputs and outputs
	MultiplierDataPath["req_msg"] = split["in"]
	MultiplierDataPath["b_sel"] = bmux["sel"]
	MultiplierDataPath["a_sel"] = amux["sel"]
	MultiplierDataPath["r_sel"] = rmux["sel"]
	MultiplierDataPath["add_sel"] = addmux["sel"]
	MultiplierDataPath["clk"] = breg["clk"]
	MultiplierDataPath["lsb"] = comp["out"]
	MultiplierDataPath["resp_msg"] = rreg["out"]

	return MultiplierDataPath

def Multiplier():
	# instantiate module
	Multiplier = Module(
		{
			"req_msg"  : 64,
			"resp_rdy" : 1,
			"req_val"  : 1,
			"clk"      : 1
		}, {
			"resp_msg" : 32,
			"req_rdy"  : 1, 
			"resp_val" : 1
		}
	)

	# initialize wires
	bsel = Wire(1)
	asel = Wire(1)
	rsel = Wire(1)
	addsel = Wire(1)
	lsb = Wire(1)

	# initialize components
	dpath = MultiplierDataPath()
	controlfsm = MultiplierControlFSM()

	# connect everything together
	dpath["b_sel"] = bsel
	dpath["a_sel"] = asel
	dpath["r_sel"] = rsel
	dpath["add_sel"] = addsel
	dpath["lsb"] = lsb

	controlfsm["b_sel"] = bsel
	controlfsm["a_sel"] = asel
	controlfsm["r_sel"] = rsel
	controlfsm["add_sel"] = addsel
	controlfsm["lsb"] = lsb

	dpath["clk"] = controlfsm["clk"] = Wire(1)

	# add components to module
	Multiplier.add_component(dpath)
	Multiplier.add_component(controlfsm)

	Multiplier["req_val"] = controlfsm["req_val"]
	Multiplier["resp_rdy"] = controlfsm["resp_rdy"]
	Multiplier["req_msg"] = dpath["req_msg"]
	Multiplier["clk"] = dpath["clk"]
	Multiplier["resp_val"] = controlfsm["resp_val"]
	Multiplier["req_rdy"] = controlfsm["req_rdy"]
	Multiplier["resp_msg"] = dpath["resp_msg"]

	return Multiplier