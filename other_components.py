from basic_parts import *

class Mux(Component):
	def __init__(self, num_inputs, input_size):
		self.mux_num_inputs = num_inputs
		self.mux_size = input_size
		c = 0
		inpts = num_inputs
		while inpts / 2 != 0:
			inpts /= 2
			c += 1
		inputs = {"sel" : c}
		outputs = {"out" : input_size}
		for i in range(num_inputs):
			inputs[i] = input_size
		Component.__init__(self, inputs, outputs)

	def update(self):
		sel = self.input_state["sel"]
		if sel == None:
			self["out"].set_value(None)
			return

		self["out"].set_value(self.input_state[sel])

