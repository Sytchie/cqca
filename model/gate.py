#!/usr/local/bin/python3

from abc import ABC, abstractmethod


class Gate(ABC):
    def __init__(self, coeff=1):
        self.coeff = coeff

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def combine(self, gate):
        pass


class Identity(Gate):
    def __str__(self):
        return " "

    def combine(self, gate):
        new_coeff = self.coeff * gate.coeff

        if isinstance(gate, Identity):
            return Identity(new_coeff)
        if isinstance(gate, PauliX):
            return PauliX(new_coeff)
        if isinstance(gate, PauliY):
            return PauliY(new_coeff)
        if isinstance(gate, PauliZ):
            return PauliZ(new_coeff)

        return None


class PauliX(Gate):
    def __str__(self):
        return "X"

    def combine(self, gate):
        new_coeff = self.coeff * gate.coeff

        if isinstance(gate, Identity):
            return PauliX(new_coeff)
        if isinstance(gate, PauliX):
            return Identity(new_coeff)
        if isinstance(gate, PauliY):
            return PauliZ(new_coeff)
        if isinstance(gate, PauliZ):
            return PauliY(new_coeff * 1j)

        return None


class PauliY(Gate):
    def __str__(self):
        return "Y"

    def combine(self, gate):
        new_coeff = self.coeff * gate.coeff

        if isinstance(gate, Identity):
            return PauliY(new_coeff)
        if isinstance(gate, PauliX):
            return PauliZ(new_coeff)
        if isinstance(gate, PauliY):
            return Identity(new_coeff)
        if isinstance(gate, PauliZ):
            return PauliX(new_coeff)

        return None


class PauliZ(Gate):
    def __str__(self):
        return "Z"

    def combine(self, gate):
        new_coeff = self.coeff * gate.coeff

        if isinstance(gate, Identity):
            return PauliZ(new_coeff)
        if isinstance(gate, PauliX):
            return PauliY(new_coeff * 1j)
        if isinstance(gate, PauliY):
            return PauliX(new_coeff)
        if isinstance(gate, PauliZ):
            return Identity(new_coeff)

        return None


def create_gates(n, coeff=1, gate_type=Identity):
    return [gate_type(coeff) for _ in range(n)]
