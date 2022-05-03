#!/usr/local/bin/python3

from copy import deepcopy
from model.gates import *

class Lattice:
    def __init__(self, cells, rules):
        self.cells = cells
        self.rules = rules
    
    def __str__(self):
        res = ""
        
        for coeff, gate in self.cells:
            res += str(coeff) + str(gate) + " "
        
        return res[: -1]
    
    def step(self):
        orig_len = len(self.cells)
        _, left_extension = self.rules[type(self.cells[0][1])]
        right_gates, right_offset = self.rules[type(self.cells[-1][1])]
        right_extension = len(right_gates) - right_offset - 1
        self.cells = \
            self.create_gate_list((1, Identity), left_extension) \
            + self.cells \
            + self.create_gate_list((1, Identity), right_extension)
        new_cells = self.create_gate_list((1, Identity), len(self.cells))

        for cell_index in range(left_extension, orig_len + left_extension):            
            gates, offset = self.rules[type(self.cells[cell_index][1])]

            for gate_index in range(len(gates)):
                coeff, gate = gates[gate_index]
                index = cell_index + gate_index - offset
                cell_coeff, cell_gate = new_cells[index]

                new_cells[index] = (coeff * cell_coeff, cell_gate.combine(gate()))
        
        self.cells = new_cells

    def create_gate_list(self, data, n):
        coeff, gate_type = data
        res = []
        
        for i in range(n):
            res.append((coeff, gate_type()))
        
        return res
