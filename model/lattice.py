#!/usr/local/bin/python3

from model.gates import *

class Lattice:
    def __init__(self, cells, rules):
        self.cells = cells
        self.rules = rules
    
    def __str__(self):
        res = ""
        
        for gate in self.cells:
            res += str(gate) + " "
        
        return res[: -1]
    
    def step(self):
        orig_len = len(self.cells)
        _, left_extension = self.rules[type(self.cells[0])]
        right_gates, right_offset = self.rules[type(self.cells[-1])]
        right_extension = len(right_gates) - right_offset - 1
        self.cells = \
            self.create_gate_list(left_extension) \
            + self.cells \
            + self.create_gate_list(right_extension)
        new_cells = self.create_gate_list(len(self.cells))

        for cell_index in range(left_extension, orig_len + left_extension):            
            gates, offset = self.rules[type(self.cells[cell_index])]

            for gate_index in range(len(gates)):
                index = cell_index + gate_index - offset

                new_cells[index] = new_cells[index].combine(gates[gate_index])
        
        self.cells = new_cells

    def create_gate_list(self, n, coeff=1, gate=Identity):
        res = []
        
        for i in range(n):
            res.append(gate(coeff))
        
        return res
