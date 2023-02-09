from abc import ABC, abstractmethod

class AbstractQuantumRegister(ABC):
    @abstractmethod
    def __init__(self,nbqubit:int, batchsize:int) -> None: pass
    def measureAll(self): pass
    def rz(self,q:int,theta): pass
    def sx(self,q:int): pass
    def cz(self,q0:int,q1:int): pass