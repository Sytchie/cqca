#!/usr/local/bin/python3

import numpy as np
from abc import ABC, abstractmethod


class Gate(ABC):
    def __init__(self, coeff=1):
        self.coeff = coeff

    @abstractmethod
    def __call__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def combine(self, gate):
        pass


class Identity(Gate):
    def __call__(self):
        super().__call__()

        return np.array([[1, 0], [0, 1]])

    def __str__(self):
        super().__str__()

        # return str(self.coeff) + "I"
        return ""

    def combine(self, gate):
        super().combine(gate)

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
    def __call__(self):
        super().__call__()

        return np.array([[1, 0], [0, 1]])

    def __str__(self):
        super().__str__()

        return str(self.coeff) + "X"

    def combine(self, gate):
        super().combine(gate)

        new_coeff = self.coeff * gate.coeff

        if isinstance(gate, Identity):
            return PauliX(new_coeff)
        if isinstance(gate, PauliX):
            return Identity(new_coeff)
        if isinstance(gate, PauliY):
            return PauliZ(new_coeff)
        if isinstance(gate, PauliZ):
            return PauliY(new_coeff)

        return None


class PauliY(Gate):
    def __call__(self):
        super().__call__()

        return 1j * np.array([[0, -1], [1, 0]])

    def __str__(self):
        super().__str__()

        return str(self.coeff) + "Y"

    def combine(self, gate):
        super().combine(gate)

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
    def __call__(self):
        super().__call__()

        return np.array([[1, 0], [0, -1]])

    def __str__(self):
        super().__str__()

        return str(self.coeff) + "Z"

    def combine(self, gate):
        super().combine(gate)

        new_coeff = self.coeff * gate.coeff

        if isinstance(gate, Identity):
            return PauliZ(new_coeff)
        if isinstance(gate, PauliX):
            return PauliY(new_coeff)
        if isinstance(gate, PauliY):
            return PauliX(new_coeff)
        if isinstance(gate, PauliZ):
            return Identity(new_coeff)

        return None


def create_gates(n, coeff=1, gate_type=Identity):
    return [gate_type(coeff) for _ in range(n)]
