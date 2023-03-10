import numpy as np
from abstractQregister import AbstractQuantumRegister
class QuantumRegister(AbstractQuantumRegister):
    batchcapable = False
    def __init__(self,nbqubit:int, batchsize:int=1) -> None:
        self.nbqubit = nbqubit
        self.qstate = np.zeros((2,)*nbqubit, dtype=np.csingle)
        self.qstate[(0,)*nbqubit] = 1
        

    
    def _oneQubitGate(self, matrix,q:int):
        assert q<self.nbqubit
        self.qstate=np.tensordot(matrix,self.qstate,(1,q))
        self.qstate=np.moveaxis(self.qstate,0,q)        
        
        # self.inQstate, self.outQstate = self.outQstate, self.inQstate

    def _twoQubitGate(self, tensor, q0:int, q1:int):
        self.qstate=np.tensordot(tensor, self.qstate, ((2,3),(q0, q1)))
        self.qstate=np.moveaxis(self.qstate,(0,1),(q0,q1))

    def measureAll(self):
        self.qstate = np.abs(self.qstate)**2
        # self.qstate = np.square(np.abs(self.qstate))
        return self.qstate.ravel()
    
    def rz(self,q:int,theta:float):
        self._oneQubitGate(RZgate(theta),q)
    
    def sx(self,q:int):
        self._oneQubitGate(SXgate,q)
        
    def cz(self,q0,q1):
        self._twoQubitGate(CZ_tensor,q0,q1)
        
    def viewQuantumState(self):
        return self.qstate.ravel()
    
    
        
def RZgate(t:float):
    return np.array([
        [np.cos(t/2) - 1j*np.sin(t/2), 0.], 
        [0,  np.cos(t/2) + 1j*np.sin(t/2)]
                     ],dtype=np.csingle)

SXgate = np.array([[1+1j, 1-1j], [1-1j, 1+1j]], dtype=np.csingle)/2

CNOT_matrix = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 1],
                        [0, 0, 1, 0]])

CNOT_tensor = np.reshape(CNOT_matrix, (2, 2, 2, 2))

CZ_matrix = np.diag([1,1,1,-1])
CZ_tensor = np.reshape(CZ_matrix, (2, 2, 2, 2))

