#!/usr/local/bin/python3

from copy import deepcopy

import util
from model.cell import Cell, create_cells, entangle, get_gates
from model.gate import Identity

class Lattice:
    def __init__(self, gates, rules, entanglement=False):
        self.cells = [Cell(gate) for gate in gates]
        self.rules = rules
        self.entanglement = entanglement
        
        if entanglement and self.cells:
            for cell in self.cells:
                entangle(self.cells[0], cell)
    
    def step(self):
        cur_len = len(self.cells)
        
        if cur_len == 0:
            return []
        
        cur_gates = get_gates(self.cells)
        _, left_extension = self.rules[type(self.cells[0].gate)]
        right_gates, right_offset = self.rules[type(self.cells[-1].gate)]
        right_extension = len(right_gates) - right_offset - 1
        
        for cell in self.cells:
            cell.gate = Identity()
        
        entanglement_target = self.cells[0] if self.entanglement else None
        
        self.cells = \
            create_cells([1] * left_extension, entanglement_target) \
            + self.cells \
            + create_cells([1] * right_extension, entanglement_target)
        
        for i in range(cur_len):
            gates, offset = self.rules[type(cur_gates[i])]
            
            for gate_index in range(len(gates)):
                index = i + left_extension + gate_index - offset
                self.cells[index].gate = self.cells[index].gate.combine(gates[gate_index])
        
        return left_extension, right_extension

    def iterate(self, n=1):
        res = [deepcopy(self.cells)]
        
        for _ in range(n):
            left_extension, right_extension = self.step()
            
            for i in range(len(res)):
                res[i] = \
                    create_cells([1] * left_extension) \
                    + res[i] \
                    + create_cells([1] * right_extension)
            
            res.append(deepcopy(self.cells))
        
        return res
