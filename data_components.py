from basic_parts import *

class Register8Bit(Component):
	def __init__(self):
		self.prev_clk = None
		self.data = None
		inputs = {"enable" : 1, "data" : 8, "clk" : 1}
		outputs = {"out" : 8}
		Component.__init__(self, inputs, outputs)

	def update(self):
		if self.prev_clk == 0 and self.input_state["clk"] == 1 and self.input_state["enable"] == 1:
			self.data = self.input_state["data"]
			self["out"].set_value(self.data)
		self.prev_clk = self.input_state["clk"]

class Register32Bit(Component):
	def __init__(self):
		self.prev_clk = None
		self.data = None
		inputs = {"enable" : 1, "data" : 32, "clk" : 1}
		outputs = {"out" : 32}
		Component.__init__(self, inputs, outputs)

	def update(self):
		if self.prev_clk == 0 and self.input_state["clk"] == 1 and self.input_state["enable"] == 1:
			self.data = self.input_state["data"]
			self["out"].set_value(self.data)
		self.prev_clk = self.input_state["clk"]

# word addressable data ram with 4mb of storage (32-bit addressable, 4-byte words)
class DataRam4MB(Component):
	def __init__(self):
		self.data = {}
		self.prev_clk = None
		inputs = {"addr" : 32, "input_data" : 32, "enable" : 1, "clk" : 1}
		outputs = {"output_data" : 32}
		Component.__init__(self, inputs, outputs)

	def update(self):
		if self.prev_clk == 0 and self.input_state["clk"] == 1:
			address = self.input_state["addr"] >> 2

			if self.input_state["enable"] == 1:
				self.data[address] = self.input_state["input_data"]
			else:
				if self.data.get(address) == None:
					self.data[address] = 0
			self["output_data"].set_value(self.data[address])
		self.prev_clk = self.input_state["clk"]

# 16 word regfile with 2 read ports and 1 write port, combinational r/w (4-byte words)
class RegisterFile64B(Component):
	def __init__(self):
		self.data = 16*[0]
		self.prev_clk = None
		inputs = {"addr_A" : 4, "addr_B" : 4, "data" : 32, "addr" : 4, "enable" : 1}
		outputs = {"out_A" : 32, "out_B" : 32}
		Component.__init__(self, inputs, outputs)

	def update(self):
		if self.input_state["enable"] == 1 and self.input_state["data"] != None and self.input_state["addr"] != None:
			address = self.input_state["addr"]
			self.data[address] = self.input_state["data"]
		elif self.input_state["enable"] == 0 and self.input_state["addr_A"] != None and self.input_state["addr_B"] != None:
			addr_A = self.input_state["addr_A"]
			addr_B = self.input_state["addr_B"]
			self["out_A"].set_value(self.data[addr_A])
			self["out_B"].set_value(self.data[addr_B])
