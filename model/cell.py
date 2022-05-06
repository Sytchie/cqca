#!/usr/local/bin/python3

from model.gate import Identity


class Cell:
    def __init__(self, gate):
        self.gate = gate
        self.entanglements = []

    def __str__(self):
        return str(self.gate)


def create_cells(coeffs, entanglement_target=None):
    cells = [Cell(Identity(coeff)) for coeff in coeffs]

    if entanglement_target is not None:
        for cell in cells:
            entangle(entanglement_target, cell)

    return cells


def get_gates(cells):
    return [cell.gate for cell in cells]


def entangle(cell_a, cell_b):
    cell_a.entanglements += [cell for cell in cell_b.entanglements + [cell_b]
                             if cell not in cell_a.entanglements and cell is not cell_a]
    cell_b.entanglements += [cell for cell in cell_a.entanglements + [cell_a]
                             if cell not in cell_b.entanglements and cell is not cell_b]
