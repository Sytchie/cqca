#!/usr/local/bin/python3

import util

class Lattice:
    def __init__(self, cells, rules):
        self.cells = cells
        self.rules = rules
    
    def step(self):
        orig_len = len(self.cells)
        
        if orig_len == 0:
            return []
        
        _, left_extension = self.rules[type(self.cells[0])]
        right_gates, right_offset = self.rules[type(self.cells[-1])]
        right_extension = len(right_gates) - right_offset - 1
        self.cells = \
            util.create_gate_list(left_extension) \
            + self.cells \
            + util.create_gate_list(right_extension)
        new_cells = util.create_gate_list(len(self.cells))

        for cell_index in range(left_extension, orig_len + left_extension):
            gates, offset = self.rules[type(self.cells[cell_index])]
            new_cells[cell_index].coeff *= self.cells[cell_index].coeff

            for gate_index in range(len(gates)):
                index = cell_index + gate_index - offset
                new_cells[index] = new_cells[index].combine(gates[gate_index])
        
        self.cells = new_cells
        
        return left_extension, right_extension

    def iterate(self, n=1):
        res = [self.cells.copy()]
        
        for _ in range(n):
            left_extension, right_extension = self.step()
            
            for i in range(len(res)):
                res[i] = \
                    util.create_gate_list(left_extension) \
                    + res[i] \
                    + util.create_gate_list(right_extension)
            
            res.append(self.cells.copy())
        
        return res
