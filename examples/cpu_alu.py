import sys
sys.path.insert(0, '../src')

from pylogic import *

# 8 bit ALU, supports the following operations:
#
#   opcode   |   op   |       func        |
# - - - - - - - - - - - - - - - - - - - - -
#    000     |  ADD   |       A + B       |
#    001     |  SUB   |       A - B       |
#    010     |  SRA   |  A >> 1 (signed)  |
#    011     |  SRL   | A >> 1 (unsigned) |
#    100     |  SLL   |       A << 1      |
#    101     |  AND   |       A & B       |
#    110     |  OR    |       A | B       |
#    111     |  NOT   |        ~A         |
def ALU8Bit():
	alu = Module(
		{ # INPUTS
			"A"  : 8, # A input
			"B"  : 8, # B input
			"Op" : 3  # opcode
		}, 

		{ # OUTPUTS
			"Y"  : 8, # result
			"C"  : 1, # carry bit
			"V"  : 1, # overflow bit
			"N"  : 1, # negative bit
			"Z"  : 1  # zero bit
		}
	)

	# make wires
	A = Wire(8)
	B = Wire(8)
	Y = Wire(8)
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
		A[0], 
		A[0], 
		A[7], 
		Wire(1, 0), 
		Wire(1, 0), 
		Wire(1, 0)
	]
	OpCode = Wire(3)

	# main components
	and0 = And(2, 8)
	or0 = Or(2, 8)
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
	zero = Comparator(8)

	# overflow check components
	xor0 = Xor(2, 1)
	xor1 = Xnor(2, 1)
	and1 = And(2, 1)
	xor2 = Xor(2, 1)
	xor3 = Xnor(2, 1)
	and2 = And(2, 1)

	# add components to module
	components = [
		adder0, adder1, sra, srl, sll, not0, not1, mux0, mux1,
		mux2, zero, xor0, xor1, and1, xor2, xor3, and2, and0, or0
	]
	labels = [
		"adder0", "adder1", "sra", "srl", "sll", "not0", 
		"not1", "mux0", "mux1", "mux2", "zero", "xor0", 
		"xor1", "and1", "xor2", "xor3", "and2", "and0", "or0"
	]
	for i in range(len(components)):
		alu.add_component(components[i])
		components[i].label = labels[i]
	
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
	sra["shift"] = Wire(1, 1)

	# SRL
	srl["A"] = A
	srl["out"] = Yop[3]
	srl["shift"] = Wire(1, 1)

	# SLL
	sll["A"] = A
	sll["out"] = Yop[4]
	sll["shift"] = Wire(1, 1)

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
	xor0[0] = A[7]
	xor0[1] = adder0["S"][7]
	xor0["out"] = Wire(1)
	xor1[0] = A[7]
	xor1[1] = B[7]
	xor1["out"] = Wire(1)
	and1[0] = xor0["out"]
	and1[1] = xor1["out"]
	and1["out"] = Vop[0]

	xor2[0] = A[7]
	xor2[1] = adder1["S"][7]
	xor2["out"] = Wire(1)
	xor3[0] = A[7]
	xor3[1] = not1["out"][7]
	xor3["out"] = Wire(1)
	and2[0] = xor2["out"]
	and2[1] = xor3["out"]
	and2["out"] = Vop[1]

	# assign inputs and outputs
	alu["A"] = A
	alu["B"] = B
	alu["Op"] = OpCode
	alu["Y"] = Y
	alu["C"] = C
	alu["V"] = V
	alu["N"] = Y[7]
	alu["Z"] = Z

	return alu
