from basic_parts import *

class Adder(Component):
	def __init__(self, input_size):
		inputs = {"A" : input_size, "B" : input_size, "Ci" : 1}
		outputs = {"S" : input_size, "Co" : 1}
		Component.__init__(self, inputs, outputs)

	def update(self):
		if self.input_state["A"] == None or self.input_state["B"] == None or self.input_state["Ci"] == None:
			result = None
		else:
			result = self.input_state["A"] + self.input_state["B"] + self.input_state["Ci"]
		self["S"].set_value(result)

class ShiftRightLogical(Component):
	def __init__(self, input_size, shift_size):
		inputs = {"A" : input_size, "shift" : shift_size}
		outputs = {"out" : input_size}
		Component.__init__(self, inputs, outputs)

	def update(self):
		if self.input_state["A"] == None or self.input_state["shift"] == None:
			result = None
		else:
			result = self.input_state["A"] >> self.input_state["shift"]
		self["out"].set_value(result)

class ShiftLeftLogical(Component):
	def __init__(self, input_size, shift_size):
		inputs = {"A" : input_size, "shift" : shift_size}
		outputs = {"out" : input_size}
		Component.__init__(self, inputs, outputs)

	def update(self):
		if self.input_state["A"] == None or self.input_state["shift"] == None:
			result = None
		else:
			result = self.input_state["A"] << self.input_state["shift"]
		self["out"].set_value(result)

class ShiftRightArithmetic(Component):
	def __init__(self, input_size, shift_size):
		inputs = {"A" : input_size, "shift" : shift_size}
		outputs = {"out" : input_size}
		Component.__init__(self, inputs, outputs)

	def update(self):
		if self.input_state["A"] == None or self.input_state["shift"] == None:
			result = None
		else:
			msb = self.inputs["A"] - 1
			size = self.inputs["A"]
			if ((self.input_state["A"] >> msb) & 1) == 1:
				val = self.input_state["A"] - 2**size
			else:
				val = self.input_state["A"]
			result = val >> self.input_state["shift"]
		self["out"].set_value(result)

class Comparator32Bit(Component):
	def __init__(self):
		Component.__init__(self, {"A" : 32, "B" : 32}, {"out" : 1})

	def update(self):
		self["out"].set_value(int(self.input_state["A"] == self.input_state["B"]))

class Comparator(Component):
	def __init__(self, size):
		Component.__init__(self, {"A" : size, "B" : size}, {"out" : 1})

	def update(self):
		self["out"].set_value(int(self.input_state["A"] == self.input_state["B"]))