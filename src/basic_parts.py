class Component(object):
	# inputs and outputs are dictionaries with (io_name -> number of bits)
	# io_state contains wire values from previous update
	# io_wires contain wires for each io
	def __init__(self, inputs, outputs, label=None):
		self.label = label
		self.inputs = inputs
		self.outputs = outputs
		self.input_state = {}
		self.output_state = {}
		self.input_wire = {}
		self.output_wire = {}

		for key in inputs:
			self.input_state[key] = None
			self.input_wire[key] = Wire(self.inputs[key])
		for key in outputs:
			self.output_state[key] = None
			self.output_wire[key] = Wire(self.outputs[key])

	# returns size of the input
	def input_size(self, key):
		return self.inputs.get(key)

	# returns size of the output
	def output_size(self, key):
		return self.outputs.get(key)

	# get input value using indexing
	def __getitem__(self, key):
		if self.input_wire.get(key) != None:
			return self.input_wire[key]
		if self.output_wire.get(key) != None:
			return self.output_wire[key]

	# assignment using indexing
	def __setitem__(self, key, wire):
		if key in self.input_wire and self.inputs[key] == wire.size():
			self.input_wire[key] = wire
		elif key in self.output_wire and self.outputs[key] == wire.size():
			self.output_wire[key] = wire
		else:
			name = self.label if self.label is not None else str(self)
			if key in self.inputs:
				io = self.inputs[key]
			elif key in self.outputs:
				io = self.outputs[key]
			else:
				print "no such io for [%s]: %s" % (name, str(key))
				return
			print "size mismatch for [%s]: got %i, expected %i" % (name, wire.size(), io)

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
	# object used to specify ranges of bits when
	# splicing wires together. Specifies the parent wire
	# and mapping of bits from the child wire to the parent wire.
	class Partition(object):
		def __init__(self, parent, start, stop):
			self.parent = parent
			self.pstart, self.pstop = start, stop
			self.start, self.stop = start - stop, 0

	# bits is the number of bits for the wire
	# value can be undefined
	def __init__(self, bits, value=None):
		self.value = value
		self.bits = bits
		self.partitions = []

	# sets the size of the wire
	def set_size(self, size):
		self.bits = size

	# returns size in bits of the wire
	def size(self):
		return self.bits

	# returns value of a single bit
	def get_bit(self, i):
		if self.value is None:
			return None

		return (self.value >> i) & 1

	# sets a single bit
	def set_bit(self, i, val):
		if self.value is None:
			return

		self.value &= ~(1 << i)
		self.value |= (1 if val else 0) << i

	# sets value of the wire
	def set_value(self, value):
		self.value = value

	# gets value of wire truncated to fit number of bits
	def get_value(self):
		mask = 2**self.bits - 1
		if not self.partitions:
			return self.value & mask if self.value is not None else None

		self.value = 0
		d = {}
		for partition in self.partitions:
			myrange = range(partition.stop, partition.start + 1)
			parentrange = range(partition.pstop, partition.pstart + 1)
			parent = partition.parent
			parent.get_value()

			for i in range(len(myrange)):
				if myrange[i] not in d:
					d[myrange[i]] = 1
				else:
					d[myrange[i]] += 1
				self.set_bit(myrange[i], parent.get_bit(parentrange[i]))

		for i in range(self.bits):
			if i not in d or d[i] != 1:
				self.value = None
				print "Wire splice mismatch"
			else:
				del d[i]

		if len(d) != 0:
			self.value = None
			print "Wire splice mismatch"

		if self.value is not None:
			return self.value & mask
		return self.value

	# get bit or slice with lsb ordering
	def __getitem__(self, key):
		if type(key) == slice:
			assert key.start >= key.stop and 0 <= key.start < self.bits and 0 <= key.stop < self.bits, "Wire splice out of bounds"
		if type(key) == int:
			assert key < self.bits, "Wire splice out of bounds"

		if type(key) == slice:
			newwire = Wire(key.start - key.stop + 1)
			newwire.partitions += [self.Partition(self, key.start, key.stop)]
			return newwire

		elif type(key) == int:
			newwire = Wire(1)
			newwire.partitions += [self.Partition(self, key, key)]
			return newwire

	# set bits or slice with lsb ordering
	def __setitem__(self, key, value):
		assert type(value) == Wire, "Wire splice must be set to a wire"
		if type(key) == slice:
			assert key.start >= key.stop and 0 <= key.start < self.bits and 0 <= key.stop < self.bits, "Wire splice out of bounds"
			assert value.bits == key.start - key.stop + 1, "Wire splice mismatch"
		if type(key) == int:
			assert key < self.bits, "Wire splice out of bounds"

		if type(key) == slice:
			partition = self.Partition(value, value.bits - 1, 0)
			partition.start = key.start
			partition.stop = key.stop
			self.partitions += [partition]

		elif type(key) == int:
			partition = self.Partition(value, 0, 0)
			partition.start = key
			partition.stop = key
			self.partitions += [partition]

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
	def __init__(self, inputs, outputs):
		Component.__init__(self, inputs, outputs)
		self.components = []

	# adds component to the module
	def add_component(self, component):
		self.components += [component]

	# traverse through tree of wires and replace identical wires 
	# in partitions
	def traverse_wires(self, root, oldwire, newwire):
		for partition in root.partitions:
			self.traverse_wires(partition.parent, oldwire, newwire)
			if partition.parent is oldwire:
				partition.parent = newwire

	# sets io by looking at every io of inner components
	def __setitem__(self, key, wire):
		prevwire = self[key]

		# search for identical wire in components as well as
		# spliced wires
		for component in self.components:
			for inpt in component.input_wire:
				self.traverse_wires(component[inpt], prevwire, wire)
				if component[inpt] is prevwire:
					component[inpt] = wire
			for outpt in component.output_wire:
				self.traverse_wires(component[outpt], prevwire, wire)
				if component[outpt] is prevwire:
					component[outpt] = wire

		# search input and outputs for identical wire
		for inpt in self.input_wire:
			self.traverse_wires(self[inpt], prevwire, wire)
			if self[inpt] is prevwire:
				if self[inpt].partitions:
					wire.partitions = self[inpt].partitions
				Component.__setitem__(self, inpt, wire)
		for outpt in self.output_wire:
			self.traverse_wires(self[outpt], prevwire, wire)
			if self[outpt] is prevwire:
				if self[outpt].partitions:
					wire.partitions = self[outpt].partitions
				Component.__setitem__(self, outpt, wire)

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
		self.tracer = {}
		self.labels = []
		self.clk = Wire(1, 1)
		self.clk_period = 1
		self.cycle = 0
		self.enable_trace = False

	# adds a component to the circuit
	def add_component(self, component):
		self.components += [component]

	# sets the clock period
	def set_clock_period(self, t):
		self.clk_period = t

	# adds a wire to be printed out to the terminal
	def trace(self, component, io, label=None):
		if label is None:
			self.tracer[str(io)] = (component, io)
			self.labels += [str(io)]
		else:
			self.tracer[label] = (component, io)
			self.labels += [label]

	def clear_trace(self):
		self.tracer = {}
		self.labels = []

	def print_trace(self):
		result = str(self.cycle) + " | "
		for label in self.labels:
			component, io = self.tracer[label]
			try:
				val = hex(component[io].get_value())
			except:
				val = str(component[io].get_value())
			result += label + " : " + val + " | "
		print result

	# returns clock
	def get_clk(self):
		return self.clk

	# updates state of all components, then updates components
	# OPTIMIZE LATER
	def update(self):
		if self.cycle % self.clk_period == 0:
			self.clk.set_value(1 - self.clk.get_value())

		for component in self.components:
			component.update_state()
		for component in self.components:
			component.update()

		if self.enable_trace:
			self.print_trace()

		self.cycle += 1

	def run(self, cycles):
		for i in range(cycles):
			self.update()

			
