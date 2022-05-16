# Clifford Quantum Cellular Automata
A Clifford Quantum Cellular Automaton (CQCA) is a *globally unique* ruleset for mapping Pauli gates to a set of Pauli gates.
This ruleset is applied, at each time step, to every cell of an infinite lattice.
Each cell holds a Pauli gate.

The application of a gate to another follows following rules:
- $i \times i = I, i \in \{I, X, Y, Z\}$ (Unitary operator)
- $i \times I = I \times i = i, i \in \{I, X, Y, Z\}$ (Identity is neutral)
- $i \times j = k, i \neq j \neq k \in \{X, Y, Z\}$

Initially, all cells of the lattice are identity gates.
However, one can change some of the cells before the first iteration to form a starting configuration.
By then iterating over time steps, the configuration of the lattice changes.
The patterns in the change are discussed in this notebook.

In this notebook, the lattice is always 1-dimensional (i.e., a spin chain).

## Environment Preparation
Technical necessities for the notebook to work properly.


```python
%load_ext autoreload
%autoreload 2
```


```python
from util import list_to_str
from model.lattice import Lattice
from model.gate import Identity, PauliX, PauliY, PauliZ
```

## Example Ruleset
Rules are specified by mapping gates to a list of gates.
For each cell, the corresponding rule is applied to the cell itself, as well as its neighborhood.


```python
ruleset = {
    Identity: ([Identity()], 0),
    PauliX: ([PauliZ()], 0),
    PauliY: ([PauliZ(-1), PauliY(), PauliZ()], 1),
    PauliZ: ([PauliZ(), PauliX(), PauliZ()], 1)
}
```

### Evolution of a Pauli Z Gate
A cell containing a Z gate will contain an X gate in the next time step, and also apply a Z gate to the surrounding cells.


```python
lattice = Lattice([PauliZ()], ruleset)

res = lattice.iterate(5)

for cells in res:
    print(list_to_str(cells))
```

    					1Z					
    				1Z	1X	1Z				
    			1Z	1X	1Z	1X	1Z			
    		1Z	1X	1Z	1X	1Z	1X	1Z		
    	1Z	1X	1Z	1X	1Z	1X	1Z	1X	1Z	
    1Z	1X	1Z	1X	1Z	1X	1Z	1X	1Z	1X	1Z


### Evolution of a Pauli X Gate.
An X gate will become a Z gate.
The neighborhood is unchanged.
From the second timestep forward the lattice behaves as if it had started with a Z gate.


```python
lattice = Lattice([PauliX()], ruleset)

res = lattice.iterate(5)

for cells in res:
    print(list_to_str(cells))
```

    				1X				
    				1Z				
    			1Z	1X	1Z			
    		1Z	1X	1Z	1X	1Z		
    	1Z	1X	1Z	1X	1Z	1X	1Z	
    1Z	1X	1Z	1X	1Z	1X	1Z	1X	1Z


### Glider
Since quantum gates, especially Pauli gates, are unitary, they are able to cancel each other out into identity gates. With the right configuration, the "active" gates (i.e., those, which are not the identity gates) propagate to a certain direction, leaving behind only "inactive" identity gates.

**Example:** Starting with Pauli X and Z gates next to each other produces a basic glider.


```python
lattice = Lattice([PauliX(), PauliZ()], ruleset)

res = lattice.iterate(5)

for cells in res:
    print(list_to_str(cells))
```

    1X	1Z					
    	1X	1Z				
    		1X	1Z			
    			1X	1Z		
    				1X	1Z	
    					1X	1Z


## Fractal Behavior
The following configuration exhibits a fractal behavior.


```python
ruleset = {
    Identity: ([Identity()], 0),
    PauliX: ([PauliX(), PauliY(), PauliX()], 1),
    PauliY: ([PauliZ(-1), PauliY(), PauliZ()], 1),
    PauliZ: ([PauliX()], 0)
}
```


```python
lattice = Lattice([PauliX(), PauliY(), PauliZ(), PauliY(), PauliX()], ruleset)

res = lattice.iterate(5)

for cells in res:
    print(list_to_str(cells))
```

    					1X	1Y	1Z	1Y	1X					
    				1X	-1X	1Z	-1X	1Z	1X	1X				
    			1X	1Z	1Z	1X	1Y	1X	1Z	1Z	1X			
    		1X	1Y			-1X	1Y	1X			1Y	1X		
    	1X	-1X	1Z	1Z	1X	-1X	1Y	1X	1X	-1Z	1Z	1X	1X	
    1X	1Z	1Z			1Z		1Y		1Z			1Z	1Z	1X


## Entanglement
When the initial cells are entangled, their "reach", which may be increasing over time, entangles further cells.

**Example:** The glider entangles the cells to the right.


```python
ruleset = {
    Identity: ([Identity()], 0),
    PauliX: ([PauliZ()], 0),
    PauliY: ([PauliZ(-1), PauliY(), PauliZ()], 1),
    PauliZ: ([PauliZ(), PauliX(), PauliZ()], 1)
}
```


```python
lattice = Lattice([PauliZ(), PauliX()], ruleset, True)

res = lattice.iterate(5)

for cells in res:
    print(list_to_str(cells))

is_entangled = True

for cell in res[-1][:-1]:
    if cell not in res[-1][-1].entanglements:
        is_entangled = False
        break

print("Is the last cell entangled with all already entangled cells?", is_entangled)
```

    					1Z	1X
    				1Z	1X	
    			1Z	1X		
    		1Z	1X			
    	1Z	1X				
    1Z	1X					
    Is the last cell entangled with all already entangled cells? False



```python
ruleset = {
    Identity: ([Identity()], 0),
    PauliX: ([PauliZ(), PauliX(), PauliZ()], 1),
    PauliY: ([PauliZ(-1), PauliY(), PauliZ()], 1),
    PauliZ: ([PauliX(), PauliZ(), PauliX()], 1)
}
```


```python
lattice = Lattice([PauliX()], ruleset, True)

res = lattice.iterate(5)

for cells in res:
    print(list_to_str(cells))

is_entangled = True

for cell in res[-1][:-1]:
    if cell not in res[-1][-1].entanglements:
        is_entangled = False
        break

print("Is the last cell entangled with all already entangled cells?", is_entangled)
```

    					1X					
    				1Z	1X	1Z				
    			1X		1X		1X			
    		1Z	1X		1X		1X	1Z		
    	1X				1X				1X	
    1Z	1X	1Z		1Z	1X	1Z		1Z	1X	1Z
    Is the last cell entangled with all already entangled cells? False



```python

```
