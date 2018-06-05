from basic_parts import *

class And(Gate):
	def __init__(self, num_inputs, input_size):
		Gate.__init__(self, num_inputs, input_size)

	def update(self):
		result = 2**self.gate_size - 1
		for key in self.input_state:
			if self.input_state[key] == None:
				self["out"].set_value(None)
				return
			result &= self.input_state[key]
		self["out"].set_value(result)

class Or(Gate):
	def __init__(self, num_inputs, input_size):
		Gate.__init__(self, num_inputs, input_size)

	def update(self):
		result = 0
		for key in self.input_state:
			if self.input_state[key] == None:
				self["out"].set_value(None)
				return
			result |= self.input_state[key]
		self["out"].set_value(result)

class Not(Gate):
	def __init__(self, input_size):
		Gate.__init__(self, 1, input_size)

	def update(self):
		if self.input_state[0] == None:
			self["out"].set_value(None)
			return
		self["out"].set_value(~self.input_state[0])

class Nand(Gate):
	def __init__(self, num_inputs, input_size):
		Gate.__init__(self, num_inputs, input_size)

	def update(self):
		result = 2**self.gate_size - 1
		for key in self.input_state:
			if self.input_state[key] == None:
				self["out"].set_value(None)
				return
			result &= self.input_state[key]
		self["out"].set_value(~result)

class Nor(Gate):
	def __init__(self, num_inputs, input_size):
		Gate.__init__(self, num_inputs, input_size)

	def update(self):
		result = 0
		for key in self.input_state:
			if self.input_state[key] == None:
				self["out"].set_value(None)
				return
			result |= self.input_state[key]
		self["out"].set_value(~result)

class Xor(Gate):
	def __init__(self, num_inputs, input_size):
		Gate.__init__(self, num_inputs, input_size)

	def update(self):
		result = 0
		for key in self.input_state:
			if self.input_state[key] == None:
				self["out"].set_value(None)
				return
			result ^= self.input_state[key]
		self["out"].set_value(result)

class Xnor(Gate):
	def __init__(self, num_inputs, input_size):
		Gate.__init__(self, num_inputs, input_size)

	def update(self):
		result = 0
		for key in self.input_state:
			if self.input_state[key] == None:
				self["out"].set_value(None)
				return
			result ^= self.input_state[key]
		self["out"].set_value(~result)

