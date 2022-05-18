#!/usr/local/bin/python3

from copy import deepcopy
from util import len_min_max
from model.gate import Identity, PauliX, PauliY, PauliZ, create_gates


class Automaton:
    def __init__(self, matrix):
        self.matrix = matrix

    def __str__(self):
        return str(self.matrix)

    def get_ruleset(self):
        xtox = self.matrix[0][0]
        xtoz = self.matrix[1][0]
        xtox_len, xtoz_len, x_min, x_max = len_min_max(xtox, xtoz)
        x_rule = create_gates(x_max - x_min + 1)

        for i in range(xtox_len):
            index = xtox[i] - x_min
            x_rule[index] = x_rule[index].combine(
                PauliX())

        for i in range(xtoz_len):
            index = xtoz[i] - x_min
            x_rule[index] = x_rule[index].combine(
                PauliZ())

        ztox = self.matrix[0][1]
        ztoz = self.matrix[1][1]
        ztox_len, ztoz_len, z_min, z_max = len_min_max(ztox, ztoz)
        z_rule = create_gates(z_max - z_min + 1)

        for i in range(ztox_len):
            index = ztox[i] - z_min
            z_rule[index] = z_rule[index].combine(
                PauliX())

        for i in range(ztoz_len):
            index = ztoz[i] - z_min
            z_rule[index] = z_rule[index].combine(
                PauliZ())

        short_rule = None
        long_rule = None

        short_origin = None
        long_origin = None

        if len(x_rule) <= len(z_rule):
            short_rule = x_rule
            long_rule = z_rule

            short_origin = -x_min
            long_origin = -z_min
        else:
            short_rule = z_rule
            long_rule = x_rule

            short_origin = -z_min
            long_origin = -x_min

        y_rule = deepcopy(long_rule)

        for i in range(len(short_rule)):
            index = i + long_origin - short_origin
            y_rule[index] = y_rule[index].combine(short_rule[i])

        return {
            Identity: ([Identity()], 0),
            PauliX: (x_rule, -x_min),
            PauliY: (y_rule, long_origin),
            PauliZ: (z_rule, -z_min)
        }
