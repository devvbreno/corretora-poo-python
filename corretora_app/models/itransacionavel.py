from abc import ABC, abstractmethod

class ITransacionavel(ABC):
    @abstractmethod
    def sacar(self, valor: float):
        pass
    
    @abstractmethod
    def depositar(self, valor: float):
        pass