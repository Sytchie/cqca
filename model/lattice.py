#!/usr/local/bin/python3

import matplotlib.pyplot as plt
from copy import deepcopy
from model.cell import Cell, create_cells, get_gates, entangle_multiple
from model.gate import Identity


class Lattice:
    def __init__(self, gates, automaton, entangle=False, debug=False):
        self.cells = [Cell(gate) for gate in gates]
        self.automaton = automaton
        self.rules = self.automaton.get_ruleset()
        self.entangle = entangle
        self.debug = debug

        if self.cells and self.entangle:
            entangle_multiple(self.cells[0], self.cells)

        self.entanglement = self._calc_entanglement()

    def iterate(self, n=1, debug=False):
        def step():
            cur_len = len(self.cells)

            if cur_len == 0:
                return 0, 0

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

                    if self.entangle:
                        cur_cell.entangle(self.cells[target_index])

            for cell in self.cells:
                if type(cell.gate) == Identity:
                    cell.disentangle()

            self.entanglement = self._calc_entanglement()

            return left_extension, right_extension

        res = [(deepcopy(self.cells), self.entanglement)]

        for i in range(n):
            if debug:
                print("Iteration", i)

            left_extension, right_extension = step()
            res = [(create_cells([1] * left_extension)
                   + cells
                   + create_cells([1] * right_extension), e)
                   for cells, e in res]

            res.append((deepcopy(self.cells), self.entanglement))

        return res

    def _calc_entanglement(self):
        if not self.entangle:
            return 0

        return (max([len(cell.entanglements) for cell in self.cells]) + 1) // 2


def plot_evolution(automaton, init_config, max_t, debug=False):
    def list_to_str(l):
        return " ".join([str(e) for e in l])

    lattice = Lattice(init_config, automaton)
    res = lattice.iterate(max_t, debug)

    for cells, _ in res:
        print(list_to_str(cells))


def plot_entanglement(alms, init_config, max_t, debug=False):
    plt.xlabel("Time t")
    plt.ylabel("Entanglement E(t)")

    for alm in alms:
        a, l, m = alm

        if debug:
            print(l)

        lattice = Lattice(init_config, a, True)
        _, entanglement = zip(*lattice.iterate(max_t, debug))

        plt.plot(list(entanglement), "-" + m, label=l)

    plt.legend()
    plt.show()
