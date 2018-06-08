from multiplier import *

# control fsm
def test_controlfsm():
	controlfsm = MultiplierControlFSM()

	circ = Circuit()
	circ.set_clock_period(7)
	circ.add_component(controlfsm)

	controlfsm["clk"] = circ.get_clk()
	controlfsm["req_val"] = Wire(1, 0)
	controlfsm["resp_rdy"] = Wire(1, 0)
	controlfsm["lsb"] = Wire(1, 0)

	controlfsm["req_rdy"] = Wire(1)
	controlfsm["resp_val"] = Wire(1)
	controlfsm["b_sel"] = Wire(1)
	controlfsm["a_sel"] = Wire(1)
	controlfsm["add_sel"] = Wire(1)
	controlfsm["r_sel"] = Wire(1)

	circ.trace(controlfsm, "req_rdy")
	circ.trace(controlfsm, "req_rdy")
	circ.trace(controlfsm, "resp_val")
	circ.trace(controlfsm, "b_sel")
	circ.trace(controlfsm, "a_sel")
	circ.trace(controlfsm, "add_sel")
	circ.trace(controlfsm, "r_sel")
	circ.enable_trace = True

	circ.run(10)
	controlfsm["req_val"].set_value(1)
	circ.run(50)
	controlfsm["resp_rdy"].set_value(1)
	controlfsm["req_val"].set_value(0)
	circ.run(10)
	controlfsm["resp_rdy"].set_value(0)
	controlfsm["req_val"].set_value(1)

# data path
def test_datapath():
	dpath = MultiplierDataPath()

	circ = Circuit()
	circ.set_clock_period(6)
	circ.add_component(dpath)

	w0 = Wire(1)
	w1 = Wire(1)
	n = Not(1)

	n[0] = w0
	n["out"] = w1

	dpath["clk"] = circ.get_clk()
	dpath["b_sel"] = Wire(1, 0)
	dpath["a_sel"] = Wire(1, 0)
	dpath["r_sel"] = Wire(1, 0)
	dpath["add_sel"] = w1
	dpath["req_msg"] = Wire(64, 0xdeadbeef1234abcd)

	dpath["lsb"] = w0
	dpath["resp_msg"] = Wire(32)

	circ.add_component(n)

	circ.trace(dpath, "lsb")
	circ.trace(dpath, "resp_msg")
	circ.enable_trace = True

	dpath["b_sel"].set_value(1)
	dpath["a_sel"].set_value(1)
	dpath["r_sel"].set_value(1)
	circ.run(20)
	dpath["b_sel"].set_value(0)
	dpath["a_sel"].set_value(0)
	dpath["r_sel"].set_value(0)
	circ.run(60)
	dpath["b_sel"].set_value(None)
	dpath["a_sel"].set_value(None)
	dpath["r_sel"].set_value(None)
		

# multiplier
def test_multiplier():
	multiplier = Multiplier()

	circ = Circuit()
	circ.set_clock_period(5)
	circ.add_component(multiplier)

	multiplier["req_val"] = Wire(1, 0)
	multiplier["resp_rdy"] = Wire(1, 0)
	multiplier["req_msg"] = Wire(64, 0x0000000a0000000d)

	multiplier["resp_val"] = Wire(1)
	multiplier["req_rdy"] = Wire(1)
	multiplier["resp_msg"] = Wire(32)

	multiplier["clk"] = circ.get_clk()

	circ.trace(multiplier, "req_val")
	circ.trace(multiplier, "resp_val")
	circ.trace(multiplier, "req_rdy")
	circ.trace(multiplier, "resp_rdy")
	circ.trace(multiplier, "req_msg")
	circ.trace(multiplier, "resp_msg")
	circ.enable_trace = True

	circ.run(2)
	multiplier["req_val"].set_value(1)
	multiplier["resp_rdy"].set_value(0)
	circ.run(200)
	multiplier["req_val"].set_value(0)
	multiplier["resp_rdy"].set_value(1)
	circ.run(50)

def test_main():
	tests = [test_datapath, test_controlfsm, test_multiplier]
	for test in tests:
		test()
		print

test_main()