# PyLogic
## Overview
PyLogic is a digital logic library written in Python that allows users to construct digital logic circuits in a way that is similar to hardware description languages. There are several basic components such as the standard And, Or, Not, Xor, etc. gates as well as additional higher-level components like Muxes, and registers. Additionally, the Module component acts like any other component allowing the user to group components together and progressively build higher-level functions. 

## Example
Examples can be seen in the examples folder, but the basic idea is to create a bunch of components, connect their inputs and outputs together using wires, and add components to a circuit which then runs the simulation one step at a time. Below is a sample of how to create a fulladder circuit and run it within a circuit:

```Python
from pylogic import *

# initialize gates with 2 inputs and 1 bit operands
xor0 = Xor(2, 1)
xor1 = Xor(2, 1)
and0 = And(2, 1)
and1 = And(2, 1)
or0 = Or(2, 1)

# initialize wires as 1 bit
A = Wire(1)
B = Wire(1)
Cin = Wire(1)
Cout = Wire(1)
S = Wire(1)

# connect components
xor0[0] = A
xor0[1] = B
xor1[0] = xor0["out"]
xor1[1] = Cin
and0[0] = A
and0[1] = B
and1[0] = xor0["out"]
and1[1] = Cin
or0[0] = and1["out"]
or0[1] = and0["out"]
xor1["out"] = S
or0["out"] = Cout

# create circuit and add components to circuit
circ = Circuit()
for component in [xor0, xor1, and0, and1, or0]:
	circ.add_component(component)

# setup wire tracing
circ.trace(xor0, 0, "A")
circ.trace(xor0, 1, "B")
circ.trace(xor1, 1, "Cin")
circ.trace(xor1, "out", "S")
circ.trace(or0, "out", "Cout")
circ.enable_trace = True

# set inputs
A.set_value(0)
B.set_value(1)
Cin.set_value(1)

# run the simulation for 5 steps
circ.run(5)
```

terminal output:
```
0 | A : 0x0 | B : 0x1 | Cin : 0x1 | S : None | Cout : None | 
1 | A : 0x0 | B : 0x1 | Cin : 0x1 | S : 0x0 | Cout : None | 
2 | A : 0x0 | B : 0x1 | Cin : 0x1 | S : 0x0 | Cout : 0x1 | 
3 | A : 0x0 | B : 0x1 | Cin : 0x1 | S : 0x0 | Cout : 0x1 | 
4 | A : 0x0 | B : 0x1 | Cin : 0x1 | S : 0x0 | Cout : 0x1 | 
```

## Features
### Connecting components
Connecting components is very simple. Each component has a set of inputs and outputs which can be accessed by indexing. Each component is initialized with a default wire object at each of its inputs and outputs so the component input or output itself can be used to connect to other components or a wire object can be initialized and explicitly set to each of the components to create a connection.
``` Python
# connecting the output of an And gate to the input of a Not gate
and0 = And(2, 1)
not0 = Not(1)

# one way to connect
not0[0] = and0["out"]

# another way to connect
wire = Wire(1)
and0["out"] = wire
not0[0] = wire
```

### Wire splitting
Wires can be divided so that a single wire can be split among multiple inputs or multiple wires mapping to the same input. The ranges just need to be specified when assigning inputs or outputs.
```Python
# connecting two 4-bit wires to the same input of a not gate
not0 = Not(8)
wire0 = Wire(4)
wire1 = Wire(4)

# specify input range when assigning
not0[0][7:4] = wire1
not0[0][3:0] = wire0

# connecting single wire to multiple not gates
not0 = Not(4)
not1 = Not(4)
wire0 = Wire(8)

# specify wire range when assigning
not0[0] = wire0[7:4]
not1[0] = wire0[3:0]
```
Any arbitrary splitting is allowed so long as all wires have all bits covered:
```Python
# connecting inputs of and gate
and0 = And(2, 8)
wire0 = Wire(8)
wire1 = Wire(8)

and0[0][7:5] = wire0[2:0]
and0[0][4:1] = wire1[7:4]
and0[0][0] = Wire(1, 0)
and0[1] = wire0
```

### Modules
Modules allow users to create components of their own using available components or other modules. Below is an example of a simple module implementing the functionality of a nand gate. After a module is created, it can be used like any other component. 
```Python
from pylogic import *

# initialize module input bits and output bits
nand_module = Module(
	{ # INPUTS
		"A"   : 8, # 8-bit input
		"B"   : 8  # 8-bit input
	},

	{ # OUTPUTS
		"out" : 8  # 8-bit output
	}
)

# make wires
A = Wire(8)
B = Wire(8)
out = Wire(8)

# make components
and0 = And(2, 8)
not0 = Not(8)

# connect everything together
and0[0] = A
and0[1] = B
not0[0] = and0["out"]
not0["out"] = out

# add components to the module
nand_module.add_component(and0)
nand_module.add_component(not0)

# assign inputs and outputs of the module
nand_module["A"] = A
nand_module["B"] = B
nand_module["out"] = out

# test for correctness
circ = Circuit()
circ.add_component(nand_module)
circ.trace(nand_module, "A")
circ.trace(nand_module, "A")
circ.trace(nand_module, "out")
circ.enable_trace = True

nand_module["A"].set_value(0xff)
nand_module["B"].set_value(0x0f)

circ.run(5)
```
terminal output:
```
0 | A : 0xff | B : 0xf | out : None | 
1 | A : 0xff | B : 0xf | out : 0xf0 | 
2 | A : 0xff | B : 0xf | out : 0xf0 | 
3 | A : 0xff | B : 0xf | out : 0xf0 | 
4 | A : 0xff | B : 0xf | out : 0xf0 | 
```

### Running the simulation
Once components are connected, they must be added to a circuit in order to run the simulation. The circuit can then step through some specified number of steps before terminating.
```Python
from pylogic import *

# make component and set values
and0 = And(2, 1)
and0[0].set_value(1)
and0[1].set_value(0)

# add to circuit
circ = Circuit()
circ.add_component(and0)

# run the simulation
circ.run(5)

# check output value
print and0["out"].get_value()
```

### Wire tracing
Inputs and outputs of any component within a circuit can be traced during the simulation and printed on the terminal for each cycle, as seen in the above examples. The component as well as its input or output must be specified. An optional label can be specified as well and the default label is simply the name of the input or output.
``` Python
from pylogic import *

# make component and set values
and0 = And(2, 1)
not0 = Not(1)
not1 = Not(1)
not2 = Not(1)
not0[0] = and0["out"]
not1[0] = not0["out"]
not2[0] = not1["out"]

and0[0].set_value(1)
and0[1].set_value(0)

# add to circuit
circ = Circuit()
circ.add_component(and0)
circ.add_component(not0)
circ.add_component(not1)
circ.add_component(not2)

# run the simulation
circ.trace(and0, 0, "and0_a")
circ.trace(and0, 1, "and0_b")
circ.trace(not0, 0, "not0")
circ.trace(not1, 0, "not1")
circ.trace(not2, 0, "not2")
circ.trace(not2, "out")
circ.enable_trace = True
circ.run(6)
```
terminal output:
```
0 | and0_a : 0x1 | and0_b : 0x0 | not0 : 0x0 | not1 : None | not2 : None | out : None | 
1 | and0_a : 0x1 | and0_b : 0x0 | not0 : 0x0 | not1 : 0x1 | not2 : None | out : None | 
2 | and0_a : 0x1 | and0_b : 0x0 | not0 : 0x0 | not1 : 0x1 | not2 : 0x0 | out : None | 
3 | and0_a : 0x1 | and0_b : 0x0 | not0 : 0x0 | not1 : 0x1 | not2 : 0x0 | out : 0x1 | 
4 | and0_a : 0x1 | and0_b : 0x0 | not0 : 0x0 | not1 : 0x1 | not2 : 0x0 | out : 0x1 | 
5 | and0_a : 0x1 | and0_b : 0x0 | not0 : 0x0 | not1 : 0x1 | not2 : 0x0 | out : 0x1 | 
```

### Clock
Each circuit has a built in clock whose period can be set by the user and will toggle its value after a certain number of simulation steps. Being able to set the period of the clock is important since the critical path of the simulation must be taken into account in certain cases involving sequential logic (note that in the example above, the output of the final not gate is not resolved until 3 simulation steps have passed).
``` Python
from pylogic import *

# create circuit
circ = Circuit()

# connect components
not0 = Not(1)
not0[0] = circ.get_clk()

circ.add_component(not0)

# run the simulation
circ.trace(not0, 0, "clk")
circ.trace(not0, "out")
circ.enable_trace = True
circ.set_clock_period(3)
circ.run(6)
```
terminal output:
```
0 | clk : 0x0 | out : 0x1 | 
1 | clk : 0x0 | out : 0x1 | 
2 | clk : 0x0 | out : 0x1 | 
3 | clk : 0x1 | out : 0x0 | 
4 | clk : 0x1 | out : 0x0 | 
5 | clk : 0x1 | out : 0x0 | 
```
