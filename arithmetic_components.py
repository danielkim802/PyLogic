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