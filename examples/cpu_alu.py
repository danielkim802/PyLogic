import sys
sys.path.insert(0, '../src')

from pylogic import *

def ALU8Bit():
	alu = Module(
		{
			"A"      : 8,
			"B"      : 8,
			"OpCode" : 3
		}, {
			"Y"      : 8,
			"C"      : 1,
			"V"      : 1,
			"N"      : 1,
			"Z"      : 1
		}
	)

	# make wires
	A = Wire(8)
	A0 = Wire(1)
	A7 = Wire(1)
	B = Wire(8)
	B7 = Wire(1)
	B7not = Wire(1)
	Y = Wire(8)
	Y7 = Wire(1)
	C = Wire(1)
	V = Wire(1)
	Vop = [
		Wire(1),
		Wire(1),
	] + [Wire(1, 0)] * 6
	N = Wire(1)
	Z = Wire(1)
	Op = Wire(3)
	Yop = [
		Wire(8), 
		Wire(8), 
		Wire(8), 
		Wire(8), 
		Wire(8), 
		Wire(8), 
		Wire(8), 
		Wire(8)
	]
	Cop = [
		Wire(1), 
		Wire(1), 
		A0, 
		A0, 
		A7, 
		Wire(1, 0), 
		Wire(1, 0), 
		Wire(1, 0)
	]
	S7Add = Wire(1)
	S7Sub = Wire(1)

	# main components
	adder0 = Adder(8)
	adder1 = Adder(8)
	sra = ShiftRightArithmetic(8, 1)
	srl = ShiftRightLogical(8, 1)
	sll = ShiftLeftLogical(8, 1)
	not0 = Not(8)
	not1 = Not(8)
	mux0 = Mux(8, 8)
	mux1 = Mux(8, 1)
	mux2 = Mux(8, 1)
	splitA = Splitter8Bit()
	splitB = Splitter8Bit()
	splitBnot = Splitter8Bit()
	splitY = Splitter8Bit()
	splitSAdd = Splitter8Bit()
	splitSSub = Splitter8Bit()
	zero = Comparator(8)

	# overflow check components
	xor0 = Xor(2, 1)
	xor1 = XNor(2, 1)
	and1 = And(2, 1)
	xor2 = Xor(2, 1)
	xor3 = XNor(2, 1)
	and2 = And(2, 1)

	# splitter A
	splitA["in"] = A
	splitA[0] = A0
	splitA[7] = A7

	# splitter Y
	splitY["in"] = Y
	splitY[7] = Y7
	
	# NOT
	not0[0] = A
	not0["out"] = Yop[7]

	# ADD
	adder0["A"] = A
	adder0["B"] = B
	adder0["Ci"] = Wire(1, 0)
	adder0["S"] = Yop[0]
	adder0["Co"] = Cop[0]

	# SUB
	not1[0] = B
	not1["out"] = Wire(8)
	adder1["A"] = A
	adder1["B"] = not1["out"]
	adder1["Ci"] = Wire(1, 1)
	adder1["S"] = Yop[1]
	adder1["Co"] = Cop[1]

	# SRA
	sra["A"] = A
	sra["out"] = Yop[2]

	# SRL
	srl["A"] = A
	srl["out"] = Yop[3]

	# SLL
	sll["A"] = A
	sll["out"] = Yop[4]

	# AND
	and0[0] = A
	and0[1] = B
	and0["out"] = Yop[5]

	# OR
	or0[0] = A
	or0[1] = B
	or0["out"] = Yop[6]

	# muxes
	mux0["sel"] = mux1["sel"] = mux2["sel"] = OpCode
	for i in range(8):
		mux0[i] = Yop[i] # Y output
		mux1[i] = Cop[i] # C output
		mux2[i] = Vop[i] # V output
	mux0["out"] = Y
	mux1["out"] = C
	mux2["out"] = V

	# Z output
	zero["A"] = Wire(8, 0)
	zero["B"] = Y
	zero["out"] = Z

	# overflow detection
	splitB["in"] = B
	splitB[7] = B7
	splitBnot["in"] = not1["out"]
	splitBnot[7] = B7not
	splitSAdd["in"] = Yop[0]
	splitSAdd["out"] = S7Add
	splitSSub["in"] = Yop[1]
	splitSSub["out"] = S7Sub

	xor0[0] = A7
	xor0[1] = S7Add
	xor0["out"] = Wire(1)
	xor1[0] = A7
	xor1[1] = B7
	xor1["out"] = Wire(1)
	and1[0] = xor0["out"]
	and1[1] = xor1["out"]
	and1["out"] = Vop[0]

	xor2[0] = A7
	xor2[1] = S7Sub
	xor2["out"] = Wire(1)
	xor3[0] = A7
	xor3[1] = B7not
	xor3["out"] = Wire(1)
	and2[0] = xor2["out"]
	and2[1] = xor3["out"]
	and2["out"] = Vop[1]

	# add components
	components = [
		adder0, adder1, sra, srl, sll, not0, not1, mux0, mux1, 
		mux2, splitA, splitB, splitBnot, splitY, splitSAdd, 
		splitSSub, zero, xor0, xor1, and1, xor2, xor3, and2
	]
	for component in components:
		alu.add_component(component)

	# assign inputs and outputs
	alu.assign_input("A", adder0, "A")
	alu.assign_input("A", adder1, "A")
	alu.assign_input("A", sra, "A")
	alu.assign_input("A", srl, "A")
	alu.assign_input("A", sll, "A")
	alu.assign_input("A", and0, 0)
	alu.assign_input("A", or0, 0)
	




