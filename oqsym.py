import numpy as np

class QuantumRegister:
    def __init__(self,nbqubit:int) -> None:
        self.nbqubit = nbqubit
        self.qstate = np.zeros((2,)*nbqubit, dtype=np.csingle)
        self.qstate[(0,)*nbqubit] = 1
    
    def oneQubitGate(self, matrix,q:int):
        assert q<self.nbqubit
        self.qstate=np.tensordot(matrix,self.qstate,(1,q))
        self.qstate=np.moveaxis(self.qstate,0,q)        
        
        # self.inQstate, self.outQstate = self.outQstate, self.inQstate

    def twoQubitGate(self, tensor, q0:int, q1:int):
        self.qstate=np.tensordot(tensor, self.qstate, ((2,3),(q0, q1)))
        self.qstate=np.moveaxis(self.qstate,(0,1),(q0,q1))

    def viewQuantumState(self):
        return self.qstate.ravel()
    
    def measureAll(self):
        self.qstate = np.abs(self.qstate)**2
        return self.qstate.ravel()
    
    def rz(self,q:int,t:float):
        self.oneQubitGate(RZgate(t),q)
    
    def sx(self,q:int):
        self.oneQubitGate(SXgate,q)
        
    def cz(self,q0,q1):
        self.twoQubitGate(CZ_tensor,q0,q1)
        
    
        
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

