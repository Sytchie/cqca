#!/usr/local/bin/python3

import matplotlib.pyplot as plt
from model.automaton import Automaton
from model.lattice import Lattice


def plot_evolution(automaton, init_config, max_t, debug=False):
    def list_to_str(l):
        return " ".join([str(e) for e in l])

    a = Automaton(automaton)
    lattice = Lattice(init_config, a)
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

        automaton = Automaton(a)
        lattice = Lattice(init_config, automaton, True)
        _, entanglement = zip(*lattice.iterate(max_t, debug))

        plt.plot(list(entanglement), "-" + m, label=l)

    plt.legend()
    plt.show()
