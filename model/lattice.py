#!/usr/local/bin/python3

from copy import deepcopy
from model.cell import Cell, create_cells, entangle, entangle_multiple, get_gates
from model.gate import Identity


class Lattice:
    def __init__(self, gates, rules, entanglement=False):
        self.cells = [Cell(gate) for gate in gates]
        self.rules = rules
        self.entanglement = entanglement

        if entanglement:
            entangle_multiple(self.cells[0], self.cells)

    def step(self):
        cur_len = len(self.cells)

        if cur_len == 0:
            return []

        cur_gates = get_gates(self.cells)
        _, left_extension = self.rules[type(self.cells[0].gate)]
        right_gates, right_offset = self.rules[type(self.cells[-1].gate)]
        right_extension = len(right_gates) - right_offset - 1
        entanglements = self.cells[0].entanglements + \
            [self.cells[0]] if self.entanglement else []

        for cell in self.cells:
            cell.gate = Identity()

        self.cells = \
            create_cells([1] * left_extension, entanglements) \
            + self.cells \
            + create_cells([1] * right_extension, entanglements)

        for i in range(cur_len):
            gates, offset = self.rules[type(cur_gates[i])]

            for gate_index in range(len(gates)):
                index = i + left_extension + gate_index - offset
                self.cells[index].gate = self.cells[index].gate.combine(
                    gates[gate_index])

        return left_extension, right_extension

    def iterate(self, n=1):
        res = [deepcopy(self.cells)]

        for _ in range(n):
            left_extension, right_extension = self.step()

            res = [create_cells([1] * left_extension)
                   + cells
                   + create_cells([1] * right_extension)
                   for cells in res]

            res.append(deepcopy(self.cells))

        return res
