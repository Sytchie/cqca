#!/usr/local/bin/python3

from model.gate import Identity


class Cell:
    def __init__(self, gate):
        self.gate = gate
        self.entanglements = []

    def __str__(self):
        return str(self.gate)


def create_cells(coeffs, entanglement_targets=[]):
    cells = []
    def operation(a, b): return entangle_multiple(
        a, b) if entanglement_targets else None

    for coeff in coeffs:
        new_cell = Cell(Identity(coeff))
        operation(new_cell, cells + entanglement_targets)
        cells.append(new_cell)

    return cells


def get_gates(cells):
    return [cell.gate for cell in cells]


def entangle(cell_a, cell_b):
    cell_a.entanglements += [cell for cell in cell_b.entanglements + [cell_b]
                             if cell not in cell_a.entanglements and cell is not cell_a]
    cell_b.entanglements += [cell for cell in cell_a.entanglements + [cell_a]
                             if cell not in cell_b.entanglements and cell is not cell_b]


def entangle_multiple(target_cell, cells):
    for cell in cells:
        entangle(target_cell, cell)
