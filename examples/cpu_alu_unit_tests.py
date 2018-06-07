from cpu_alu import *

def ALU8Bit_test_add(trace=False):
	results = []

	alu = ALU8Bit()

	circ = Circuit()
	circ.add_component(alu)
	circ.trace(alu, "A")
	circ.trace(alu, "B")
	circ.trace(alu, "Op")
	circ.trace(alu, "Y")
	circ.trace(alu, "C")
	circ.trace(alu, "V")
	circ.trace(alu, "N")
	circ.trace(alu, "Z")
	circ.enable_trace = trace

	alu["Y"] = Wire(8)
	alu["C"] = Wire(1)
	alu["V"] = Wire(1)
	alu["N"] = Wire(1)
	alu["Z"] = Wire(1)

	name = 'test_add_00'
	print name
	alu["A"] = Wire(8, 0x05)
	alu["B"] = Wire(8, 0x06)
	alu["Op"] = Wire(3, 0x0)
	circ.run(5)
	results += [[
		name, 
		alu["Y"].get_value() == 0xb,
		alu["C"].get_value() == 0x0,
		alu["V"].get_value() == 0x0,
		alu["N"].get_value() == 0x0,
		alu["Z"].get_value() == 0x0
	]]

	name = 'test_add_01'
	print name
	alu["A"] = Wire(8, 0x80)
	alu["B"] = Wire(8, 0x80)
	alu["Op"] = Wire(3, 0x0)
	circ.run(5)
	results += [[
		name, 
		alu["Y"].get_value() == 0x0,
		alu["C"].get_value() == 0x1,
		alu["V"].get_value() == 0x1,
		alu["N"].get_value() == 0x0,
		alu["Z"].get_value() == 0x1
	]]

	return results

def ALU8Bit_test_sub(trace=False):
	results = []

	alu = ALU8Bit()

	circ = Circuit()
	circ.add_component(alu)
	circ.trace(alu, "A")
	circ.trace(alu, "B")
	circ.trace(alu, "Op")
	circ.trace(alu, "Y")
	circ.trace(alu, "C")
	circ.trace(alu, "V")
	circ.trace(alu, "N")
	circ.trace(alu, "Z")
	circ.enable_trace = trace

	alu["Y"] = Wire(8)
	alu["C"] = Wire(1)
	alu["V"] = Wire(1)
	alu["N"] = Wire(1)
	alu["Z"] = Wire(1)

	name = 'test_sub_00'
	print name
	alu["A"] = Wire(8, 0x05)
	alu["B"] = Wire(8, 0x04)
	alu["Op"] = Wire(3, 0x1)
	circ.run(8)
	results += [[
		name, 
		alu["Y"].get_value() == 0x1,
		alu["C"].get_value() == 0x1,
		alu["V"].get_value() == 0x0,
		alu["N"].get_value() == 0x0,
		alu["Z"].get_value() == 0x0
	]]

	return results

def ALU8Bit_test_shift(trace=False):
	results = []

	alu = ALU8Bit()

	circ = Circuit()
	circ.add_component(alu)
	circ.trace(alu, "A")
	circ.trace(alu, "B")
	circ.trace(alu, "Op")
	circ.trace(alu, "Y")
	circ.trace(alu, "C")
	circ.trace(alu, "V")
	circ.trace(alu, "N")
	circ.trace(alu, "Z")
	circ.enable_trace = trace

	alu["Y"] = Wire(8)
	alu["C"] = Wire(1)
	alu["V"] = Wire(1)
	alu["N"] = Wire(1)
	alu["Z"] = Wire(1)

	name = 'test_shift_sra_00'
	print name
	alu["A"] = Wire(8, 0xfe)
	alu["B"] = Wire(8, 0x00)
	alu["Op"] = Wire(3, 0x2)
	circ.run(3)
	results += [[
		name, 
		alu["Y"].get_value() == 0xff,
		alu["C"].get_value() == 0x0,
		alu["V"].get_value() == 0x0,
		alu["N"].get_value() == 0x1,
		alu["Z"].get_value() == 0x0
	]]

	name = 'test_shift_srl_00'
	print name
	alu["A"] = Wire(8, 0xfe)
	alu["B"] = Wire(8, 0x00)
	alu["Op"] = Wire(3, 0x3)
	circ.run(3)
	results += [[
		name, 
		alu["Y"].get_value() == 0x7f,
		alu["C"].get_value() == 0x0,
		alu["V"].get_value() == 0x0,
		alu["N"].get_value() == 0x0,
		alu["Z"].get_value() == 0x0
	]]

	name = 'test_shift_sll_00'
	print name
	alu["A"] = Wire(8, 0xff)
	alu["B"] = Wire(8, 0x00)
	alu["Op"] = Wire(3, 0x4)
	circ.run(3)
	results += [[
		name, 
		alu["Y"].get_value() == 0xfe,
		alu["C"].get_value() == 0x1,
		alu["V"].get_value() == 0x0,
		alu["N"].get_value() == 0x1,
		alu["Z"].get_value() == 0x0
	]]

	return results

def ALU8Bit_test_bitwise(trace=False):
	results = []

	alu = ALU8Bit()

	circ = Circuit()
	circ.add_component(alu)
	circ.trace(alu, "A")
	circ.trace(alu, "B")
	circ.trace(alu, "Op")
	circ.trace(alu, "Y")
	circ.trace(alu, "C")
	circ.trace(alu, "V")
	circ.trace(alu, "N")
	circ.trace(alu, "Z")
	circ.enable_trace = trace

	alu["Y"] = Wire(8)
	alu["C"] = Wire(1)
	alu["V"] = Wire(1)
	alu["N"] = Wire(1)
	alu["Z"] = Wire(1)

	name = 'test_and_00'
	print name
	alu["A"] = Wire(8, 0x05)
	alu["B"] = Wire(8, 0x06)
	alu["Op"] = Wire(3, 0x5)
	circ.run(10)
	results += [[
		name, 
		alu["Y"].get_value() == 0x04,
		alu["C"].get_value() == 0x0,
		alu["V"].get_value() == 0x0,
		alu["N"].get_value() == 0x0,
		alu["Z"].get_value() == 0x0
	]]

	name = 'test_or_00'
	print name
	alu["A"] = Wire(8, 0x05)
	alu["B"] = Wire(8, 0x06)
	alu["Op"] = Wire(3, 0x6)
	circ.run(10)
	results += [[
		name, 
		alu["Y"].get_value() == 0x05 | 0x06,
		alu["C"].get_value() == 0x0,
		alu["V"].get_value() == 0x0,
		alu["N"].get_value() == 0x0,
		alu["Z"].get_value() == 0x0
	]]

	name = 'test_not_00'
	print name
	alu["A"] = Wire(8, 0x05)
	alu["B"] = Wire(8, 0x00)
	alu["Op"] = Wire(3, 0x7)
	circ.run(10)
	results += [[
		name, 
		alu["Y"].get_value() == 0xfa,
		alu["C"].get_value() == 0x0,
		alu["V"].get_value() == 0x0,
		alu["N"].get_value() == 0x1,
		alu["Z"].get_value() == 0x0
	]]

	return results

def ALU8Bit_test():
	tests = [[], ALU8Bit_test_add, ALU8Bit_test_sub, ALU8Bit_test_shift, ALU8Bit_test_bitwise]
	results = reduce(lambda x, y: x + y(), tests)
	failed = []

	for result in results:
		if False in result:
			failed += [result]

	print
	if not failed:
		print "All tests passed!!"
	else:
		print "Failed the following tests:"
		for result in failed:
			for i in result:
				print i,
			print

ALU8Bit_test()
