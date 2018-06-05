from multiplier import *

# control fsm
def test_controlfsm():
	controlfsm = MultiplierControlFSM()

	circ = Circuit()
	circ.set_clock_period(3)
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

	circ.add_terminal_output(controlfsm["req_rdy"], "req_rdy")
	circ.add_terminal_output(controlfsm["req_rdy"], "req_rdy")
	circ.add_terminal_output(controlfsm["resp_val"], "resp_val")
	circ.add_terminal_output(controlfsm["b_sel"], "b_sel")
	circ.add_terminal_output(controlfsm["a_sel"], "a_sel")
	circ.add_terminal_output(controlfsm["add_sel"], "add_sel")
	circ.add_terminal_output(controlfsm["r_sel"], "r_sel")

	for i in range(150):
		if i == 2:
			controlfsm["req_val"].set_value(1)
		if i == 40:
			controlfsm["resp_rdy"].set_value(1)
			controlfsm["req_val"].set_value(0)
		if i == 45:
			controlfsm["resp_rdy"].set_value(0)
			controlfsm["req_val"].set_value(1)
		circ.update()

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

	circ.add_terminal_output(dpath["lsb"], "lsb")
	circ.add_terminal_output(dpath["resp_msg"], "resp_msg")

	for i in range(70):
		if i == 0:
			dpath["b_sel"].set_value(1)
			dpath["a_sel"].set_value(1)
			dpath["r_sel"].set_value(1)
		if i == 5:
			dpath["b_sel"].set_value(0)
			dpath["a_sel"].set_value(0)
			dpath["r_sel"].set_value(0)
		if i == 50:
			dpath["b_sel"].set_value(None)
			dpath["a_sel"].set_value(None)
			dpath["r_sel"].set_value(None)
		
		circ.update()

# multiplier
def test_multiplier():
	multiplier = Multiplier()

	circ = Circuit()
	circ.set_clock_period(10)
	circ.add_component(multiplier)

	multiplier["req_val"] = Wire(1, 0)
	multiplier["resp_rdy"] = Wire(1, 0)
	multiplier["req_msg"] = Wire(64, 0x0000000a0000000d)

	multiplier["resp_val"] = Wire(1)
	multiplier["req_rdy"] = Wire(1)
	multiplier["resp_msg"] = Wire(32)

	multiplier["clk"] = circ.get_clk()

	circ.add_terminal_output(multiplier["req_val"], "req_val")
	circ.add_terminal_output(multiplier["resp_val"], "resp_val")
	circ.add_terminal_output(multiplier["req_rdy"], "req_rdy")
	circ.add_terminal_output(multiplier["resp_rdy"], "resp_rdy")
	circ.add_terminal_output(multiplier["req_msg"], "req_msg")
	circ.add_terminal_output(multiplier["resp_msg"], "resp_msg")

	for i in range(70):
		if i == 2:
			multiplier["req_val"].set_value(1)
			multiplier["resp_rdy"].set_value(0)
		if i == 50:
			multiplier["req_val"].set_value(0)
			multiplier["resp_rdy"].set_value(1)

		circ.update()

def test_main():
	tests = [test_datapath, test_controlfsm, test_multiplier]
	for test in tests:
		test()
		print

test_main()