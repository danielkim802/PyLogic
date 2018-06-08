import sys
sys.path.insert(0, '../src')

from pylogic import *

# 8 bit register file with memory bank of 8 addressable registers
# 2 read ports addressable by RA and RB, outputs at A and B
# 1 write port addressable by WA with input data WD and write enable WE
def Regfile8Bit():
	regfile = Module(
		{ # INPUTS
			"RA"  : 3, # read address A
			"RB"  : 3, # read address B
			"WE"  : 1, # write enable
			"WA"  : 3, # write address
			"WD"  : 8, # write data
			"clk" : 1
		}, 

		{ # OUTPUTS
			"A"   : 8, # A register output data
			"B"   : 8  # B register output data
		}
	)

	# initialize wires
	RA = Wire(3)
	RB = Wire(3)
	WE = Wire(1)
	WA = Wire(3)
	WD = Wire(8)
	clk = Wire(1)
	A = Wire(8)
	B = Wire(8)

	# initialize components

	mem = [
		Register8Bit(),
		Register8Bit(),
		Register8Bit(),
		Register8Bit(),
		Register8Bit(),
		Register8Bit(),
		Register8Bit(),
		Register8Bit()
	]
	demux0 = Demux(8, 8)
	mux0 = Mux(8, 8)
	mux1 = Mux(8, 8)

	# connect everything together
	demux0["in"] = WD
	demux0["sel"] = WA
	mux0["sel"] = RA
	mux0["out"] = A
	mux1["sel"] = RB
	mux1["out"] = B

	for i in range(len(mem)):
		reg = mem[i]
		reg["enable"] = WE
		reg["data"] = demux0[i]
		reg["clk"] = clk
		mux0[i] = mux1[i] = reg["out"]

	# add components
	components = [demux0, mux0, mux1] + mem
	for component in components:
		regfile.add_component(component)

	# assign module inputs and outputs
	regfile["RA"] = RA
	regfile["RB"] = RB
	regfile["WE"] = WE
	regfile["WA"] = WA
	regfile["WD"] = WD
	regfile["clk"] = clk
	regfile["A"] = A
	regfile["B"] = B

	return regfile
