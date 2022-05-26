#!/usr/local/bin/python3

from model.gate import Identity


class Cell:
    def __init__(self, gate):
        self.gate = gate
        self.entanglements = []

    def __str__(self):
        return str(self.gate)

    def entangle(self, target):
        if target is self or target in self.entanglements:
            return

        self.entanglements += [target]
        target.entangle(self)

        for cell in target.entanglements:
            self.entangle(cell)

    def disentangle(self):
        for cell in self.entanglements:
            cell.entanglements.remove(self)

        self.entanglements = []


def create_cells(coeffs, entanglement_targets=[]):
    def op(a, b): return entangle_multiple(
        a, b) if entanglement_targets else None

    cells = []

    for coeff in coeffs:
        new_cell = Cell(Identity(coeff))
        op(new_cell, cells + entanglement_targets)
        cells.append(new_cell)

    return cells


def get_gates(cells):
    return [cell.gate for cell in cells]


def entangle_multiple(target_cell, cells):
    for cell in cells:
        target_cell.entangle(cell)
