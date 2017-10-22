class Component(object):
	# inputs and outputs are dictionaries with (io_name -> number of bits)
	# io_state contains wire values from previous update
	# io_wires contain wires for each io
	def __init__(self, inputs, outputs):
		self.inputs = inputs
		self.outputs = outputs
		self.input_state = {}
		self.output_state = {}
		self.input_wire = {}
		self.output_wire = {}

		for key in inputs:
			self.input_state[key] = None
			self.input_wire[key] = Wire(0)
		for key in outputs:
			self.output_state[key] = None
			self.output_wire[key] = Wire(0)

	# returns size of the input
	def input_size(self, key):
		return self.inputs[key]

	# returns size of the output
	def output_size(self, key):
		return self.outputs[key]

	# get input value using indexing
	def __getitem__(self, key):
		if self.input_wire.get(key) != None:
			return self.input_wire[key]
		if self.output_wire.get(key) != None:
			return self.output_wire[key]

	# assignment using indexing 
	def __setitem__(self, key, wire):
		if self.input_wire.get(key) != None and self.inputs[key] == wire.size():
			self.input_wire[key] = wire
		elif self.output_wire.get(key) != None and self.outputs[key] == wire.size():
			self.output_wire[key] = wire

	# updates state to reflect value of wires
	def update_state(self):
		for key in self.input_wire:
			self.input_state[key] = self.input_wire[key].get_value()
		for key in self.output_wire:
			self.output_state[key] = self.output_wire[key].get_value()

	# updates output wires based on state; every subclass must implement this function
	def update(self):
		raise NotImplementedError

class Wire(object):
	# bits is the number of bits for the wire
	# value can be undefined
	def __init__(self, bits, value=None):
		self.value = value
		self.bits = bits

	# sets the size of the wire
	def set_size(self, size):
		self.bits = size

	# returns size in bits of the wire
	def size(self):
		return self.bits

	# sets value of the wire
	def set_value(self, value):
		self.value = value

	# gets value of wire truncated to fit number of bits
	def get_value(self):
		if self.value == None:
			return None
		return self.value & (2**self.bits - 1)

	# get bit or slice with lsb ordering
	def __getitem__(self, key):
		if self.value == None:
			return None

		if isinstance(key, slice):
			return (self.value >> key.stop) & (2**(key.start - key.stop + 1) - 1)

		elif type(key) == int:
			return (self.value >> key) & 1

	# set bits or slice with lsb ordering
	def __setitem__(self, key, value):
		if self.value == None:
			return

		if isinstance(key, slice):
			mask = 2**(key.start - key.stop + 1) - 1
			self.value &= ~(mask << key.stop)
			self.value |= (value & mask) << key.stop

		elif type(key) == int:
			val = value & 1
			self.value &= ~(1 << key)
			self.value |= val << key

class Gate(Component):
	# initializes logic gate given a number of inputs and input size
	def __init__(self, num_inputs, input_size):
		self.gate_num_inputs = num_inputs
		self.gate_size = input_size
		inputs = {}
		outputs = {"out" : input_size}
		for i in range(num_inputs):
			inputs[i] = input_size
		Component.__init__(self, inputs, outputs)

class Module(Component):
	# inputs and outputs indicate size of each input/output
	# io_map maps each io to an io of an inner component
	# io_map: input key -> (component, component input key)
	def __init__(self, inputs, outputs):
		Component.__init__(self, inputs, outputs)
		self.components = []
		self.input_map = {}
		self.output_map = {}

		for key in inputs:
			self.input_map[key] = []
		for key in outputs:
			self.output_map[key] = []

	# adds component to the module
	def add_component(self, component):
		self.components += [component]

	# assigns an input of the module to an input of a component
	def assign_input(self, module_input, component, component_input):
		if component[component_input] != None and component.input_size(component_input) == self.inputs[module_input]:
			self.input_map[module_input] += [(component, component_input)]
			self.input_wire[module_input] = component[component_input]

	# assigns an output of the module to an output of a component
	def assign_output(self, module_output, component, component_output):
		if component[component_output] != None and component.output_size(component_output) == self.outputs[module_output]:
			self.output_map[module_output] += [(component, component_output)]
			self.output_wire[module_output] = component[component_output]

	# sets io through inner component using io map
	def __setitem__(self, key, wire):
		Component.__setitem__(self, key, wire)

		if self.input_map.get(key) != None and self.inputs[key] == wire.size():
			for (component, component_key) in self.input_map[key]:
				component[component_key] = wire
		if self.output_map.get(key) != None and self.outputs[key] == wire.size():
			for (component, component_key) in self.output_map[key]:
				component[component_key] = wire

	# updates state to reflect value of wires
	def update_state(self):
		Component.update_state(self)
		for component in self.components:
			component.update_state()

	# updates all components within module by one tick
	def update(self):
		for component in self.components:
			component.update()

# top-level class that holds all components and runs simulation
class Circuit(object):
	def __init__(self):
		self.components = []

	# adds a component to the circuit
	def add_component(self, component):
		self.components += [component]

	# TODO: add method for printing out useful information

	# updates state of all components, then updates components
	# OPTIMIZE LATER
	def update(self):
		for component in self.components:
			component.update_state()
		for component in self.components:
			component.update()


