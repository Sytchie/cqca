#!/usr/local/bin/python3

from copy import deepcopy
from model.cell import Cell, create_cells, get_gates
from model.gate import Identity


class Lattice:
    def __init__(self, gates, automaton, entanglement=False):
        self.cells = [Cell(gate) for gate in gates]
        self.automaton = automaton
        self.rules = self.automaton.get_ruleset()
        self.entanglement = entanglement

        if self.cells and self.entanglement:
            for cell in self.cells:
                self.cells[0].entangle(cell)

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

        self.cells = \
            create_cells([1] * left_extension) \
            + self.cells \
            + create_cells([1] * right_extension)

        for i in range(cur_len):
            cur_index = i + left_extension
            cur_cell = self.cells[cur_index]
            gates, offset = self.rules[type(cur_gates[i])]

            for gate_index in range(len(gates)):
                target_index = cur_index + gate_index - offset
                self.cells[target_index].gate = self.cells[target_index].gate.combine(
                    gates[gate_index])

                if self.entanglement:
                    cur_cell.entangle(self.cells[target_index])

        for cell in self.cells:
            if type(cell.gate) == Identity:
                cell.disentangle()

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
