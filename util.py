#!/usr/local/bin/python3

import matplotlib.pyplot as plt
from model.lattice import Lattice


def list_to_str(l):
    return "\t".join([str(e) for e in l])


def len_min_max(a, b):
    a_len = len(a)
    b_len = len(b)

    min_val = None
    max_val = None

    if a_len > 0 and b_len > 0:
        min_val = min(a[0], b[0])
        max_val = max(a[-1], b[-1])
    elif a_len > 0:
        min_val = a[0]
        max_val = a[-1]
    else:
        min_val = b[0]
        max_val = b[-1]

    return a_len, b_len, min_val, max_val


def plot_entanglement(alms, init_config, max_t):
    plt.xlabel("Time t")
    plt.ylabel("Entanglement E(t)")

    for alm in alms:
        a, l, m = alm
        lattice = Lattice(init_config, a, True)
        _, entanglements = zip(*lattice.iterate(max_t))

        plt.plot(list(entanglements), "-" + m, label=l)

    plt.legend()
    plt.show()
