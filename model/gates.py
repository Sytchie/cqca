#!/usr/local/bin/python3

from typing import Type
from abc import ABC, abstractmethod
import numpy as np

class Gate(ABC):
    @abstractmethod
    def __call__(self):
        pass
    
    @abstractmethod
    def __str__(self):
        pass
    
    @abstractmethod
    def combine(self, gate):
        #print("Combining ", self, " and ", gate)
        pass

class Identity(Gate):
    def __call__(self):
        super().__call__()
        
        return np.array([[1, 0], [0, 1]])
    
    def __str__(self):
        super().__str__()
        
        return "I"
    
    def combine(self, gate):
        super().combine(gate)
        
        return gate

class PauliX(Gate):
    def __call__(self):
        super().__call__()
        
        return np.array([[1, 0], [0, 1]])
    
    def __str__(self):
        super().__str__()
        
        return "X"
    
    def combine(self, gate):
        super().combine(gate)

        if isinstance(gate, Identity):
            return PauliX()
        if isinstance(gate, PauliX):
            return Identity()
        if isinstance(gate, PauliY):
            return PauliZ()
        if isinstance(gate, PauliZ):
            return PauliY()
        
        return None
        

class PauliY(Gate):
    def __call__(self):
        super().__call__()
        
        return 1j * np.array([[0, -1], [1, 0]])
    
    def __str__(self):
        super().__str__()
        
        return "Y"
    
    def combine(self, gate):
        super().combine(gate)
        
        if isinstance(gate, Identity):
            return PauliY()
        if isinstance(gate, PauliX):
            return PauliZ()
        if isinstance(gate, PauliY):
            return Identity()
        if isinstance(gate, PauliZ):
            return PauliX()
        
        return None

class PauliZ(Gate):
    def __call__(self):
        super().__call__()
        
        return np.array([[1, 0], [0, -1]])
    
    def __str__(self):
        super().__str__()
        
        return "Z"
    
    def combine(self, gate):
        super().combine(gate)
        
        if isinstance(gate, Identity):
            return PauliZ()
        if isinstance(gate, PauliX):
            return PauliY()
        if isinstance(gate, PauliY):
            return PauliX()
        if isinstance(gate, PauliZ):
            return Identity()
        
        return None
