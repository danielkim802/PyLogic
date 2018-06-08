from cpu_registerfile import *

def Registerfile8Bit_test_set(trace=False):
	results = []

	regfile = Regfile8Bit()

	circ = Circuit()
	circ.set_clock_period(5)
	circ.add_component(regfile)
	circ.trace(regfile, "A")
	circ.trace(regfile, "B")
	circ.trace(regfile, "RA")
	circ.trace(regfile, "RB")
	circ.trace(regfile, "WE")
	circ.trace(regfile, "WA")
	circ.trace(regfile, "WD")
	circ.trace(regfile, "clk")
	circ.enable_trace = trace

	regfile["A"] = Wire(8)
	regfile["B"] = Wire(8)
	regfile["RA"] = Wire(3)
	regfile["RB"] = Wire(3)
	regfile["WE"] = Wire(1)
	regfile["WA"] = Wire(3)
	regfile["WD"] = Wire(8)
	regfile["clk"] = circ.get_clk()

	name = 'test_write_00'
	print name
	regfile["RA"].set_value(7)
	regfile["RB"].set_value(0)
	regfile["WE"].set_value(1)
	regfile["WA"].set_value(5)
	regfile["WD"].set_value(0xea)
	circ.run(10)

	results += [[
		name, 
		regfile["A"].get_value() == 0x0,
		regfile["B"].get_value() == 0x0,
	]]

	name = 'test_write_01'
	print name
	regfile["RA"].set_value(5)
	regfile["RB"].set_value(0)
	regfile["WE"].set_value(0)
	regfile["WA"].set_value(5)
	regfile["WD"].set_value(0xff)
	circ.run(10)

	results += [[
		name, 
		regfile["A"].get_value() == 0xea,
		regfile["B"].get_value() == 0x0,
	]]

	name = 'test_read_00'
	print name
	regfile["RA"].set_value(5)
	regfile["RB"].set_value(0)
	regfile["WE"].set_value(0)
	regfile["WA"].set_value(5)
	regfile["WD"].set_value(0xea)
	circ.run(10)

	results += [[
		name, 
		regfile["A"].get_value() == 0xea,
		regfile["B"].get_value() == 0x0,
	]]

	return results

def Regfile8Bit_test():
	tests = [[], Registerfile8Bit_test_set]
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

Regfile8Bit_test()