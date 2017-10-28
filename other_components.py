from basic_parts import *

class Mux(Component):
	def __init__(self, num_inputs, input_size):
		self.mux_num_inputs = num_inputs
		self.mux_size = input_size
		c = 0
		inpts = num_inputs - 1
		while inpts != 0:
			inpts >>= 1
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

class Splitter64Bit(Component):
	def __init__(self):
		Component.__init__(self, {"in" : 64}, {"lsb" : 32, "msb" : 32})

	def update(self):
		lsb = (self.input_state["in"] & 0xffffffff) >> 32
		msb = self.input_state["in"] >> 32
		self["lsb"].set_value(lsb)
		self["msb"].set_value(msb)