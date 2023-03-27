from abc import ABC, abstractmethod

class AbstractQuantumRegister(ABC):
    @abstractmethod
    def __init__(self,nbqubit:int, batchsize:int) -> None: pass
    @abstractmethod
    def measureAll(self): pass
    @abstractmethod
    def rz(self,q:int,theta): pass
    @abstractmethod
    def sx(self,q:int): pass
    @abstractmethod
    def cz(self,q0:int,q1:int): pass