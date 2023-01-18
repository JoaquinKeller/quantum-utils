import numpy as np
import numexpr as ne

self=dict()
class QuantumRegister:
    def __init__(self, nbqubit:int, batchsize:int=1) -> None:
        self.nbqubit = nbqubit
        self.batchsize=batchsize
        self.inQ = np.zeros((2**nbqubit, batchsize), dtype=np.csingle)  # quantum state, input buffer 
        self.outQ = np.empty_like(self.inQ)
        self.reset()
    
    def reset(self):
        self.inQ.fill(0)
        self.inQ[0].fill(1)
        
    def rz(self, q:int, theta):
        assert q<self.nbqubit
        assert theta.shape == (self.batchsize,)
        # t2 = theta/2
        t2 = ne.evaluate('theta/2')
        cost = ne.evaluate('cos(t2)')
        isint = ne.evaluate('1j*sin(t2)')
        gate00 = ne.evaluate('cost - isint')
        gate11 = ne.evaluate('cost + isint')
        shape = (2**q, 2, -1, self.batchsize)
        self.inQ.shape = shape
        self.outQ.shape = shape
        q0 = self.inQ[:, 0, :]
        q1 = self.inQ[:, 1, :]
        self.outQ[:, 0, :] = ne.evaluate('gate00 * q0')
        self.outQ[:, 1, :] = ne.evaluate('gate11 * q1')

        self.inQ.shape = (-1, self.batchsize)
        self.outQ.shape = (-1, self.batchsize)
        self.inQ, self.outQ = self.outQ, self.inQ

    def rz2(self, q:int, theta):
        assert q<self.nbqubit
        assert theta.shape == (self.batchsize,)
        # t2 = theta/2
        t2 = ne.evaluate('theta/2')
        cost = ne.evaluate('cos(t2)')
        isint = ne.evaluate('1j*sin(t2)')
        gate00 = ne.evaluate('cost - isint')
        gate11 = ne.evaluate('cost + isint')
        shape = (2**q, 2, -1, self.batchsize)
        self.inQ.shape = shape
        q0 = self.inQ[:, 0, :]
        q1 = self.inQ[:, 1, :]
        self.inQ[:, 0, :] = ne.evaluate('gate00 * q0')
        self.inQ[:, 1, :] = ne.evaluate('gate11 * q1')

        self.inQ.shape = (-1, self.batchsize)
    
    
    def oneQubitGate(self,gate, qbit):
        shape = (2**qbit, 2, -1, self.batchsize)
        self.inQ.shape = shape
        self.outQ.shape = shape
        
        g00, g01, g10, g11 = gate[0, 0], gate[0, 1], gate[1, 0], gate[1, 1]
        q0,q1 = self.inQ[:, 0, :], self.inQ[:, 1, :]
        
        self.outQ[:, 0, :] = ne.evaluate('g00 * q0 + g01 * q1')
        self.outQ[:, 1, :] = ne.evaluate('g10* q0 + g11 * q1')

        self.inQ.shape = (-1, self.batchsize)
        self.outQ.shape = (-1, self.batchsize)
        self.inQ, self.outQ = self.outQ, self.inQ
    
    def oneQubitGate2(self,gate, qbit):
        shape = (2**qbit, 2, -1, self.batchsize)
        self.inQ.shape = shape
        
        g00, g01, g10, g11 = gate[0, 0], gate[0, 1], gate[1, 0], gate[1, 1]
        q0,q1 = self.inQ[:, 0, :], self.inQ[:, 1, :]
        
        self.inQ[:, 0, :], self.inQ[:, 1, :] = ne.evaluate('g00 * q0 + g01 * q1'), ne.evaluate('g10* q0 + g11 * q1')

        self.inQ.shape = (-1, self.batchsize)

    
    def oneQubitGate3(self,gate, qbit):
        shape = (2**qbit, 2, -1, self.batchsize)
        self.inQ.shape = shape
        self.outQ.shape = shape
        self.outQ[:, 0, :] = (gate[0, 0] * self.inQ[:, 0, :] +
                            gate[0, 1] * self.inQ[:, 1, :])
        self.outQ[:, 1, :] = (gate[1, 0] * self.inQ[:, 0, :] +
                            gate[1, 1] * self.inQ[:, 1, :])

        self.inQ.shape = (-1, self.batchsize)
        self.outQ.shape = (-1, self.batchsize)
        self.inQ, self.outQ = self.outQ, self.inQ
        
    
    def sx(self,q:int):
        self.oneQubitGate(SXgate,q)

    
    def sx2(self,q:int):
        self.oneQubitGate2(SXgate,q)

        
    def cz(self,q0,q1):
        """ 
        diag(1,1,1,-1)
        """
        qbit0, qbit1 = min(q0, q1), max(q0, q1)
        shape = (2**qbit0, 2, 2**(qbit1 - qbit0 - 1), 2, -1, self.batchsize)
        self.inQ.shape = shape
        self.outQ.shape = shape
        
        self.outQ[:, 0, :, 0, :] = self.inQ[:, 0, :, 0, :]
        self.outQ[:, 0, :, 1, :] = self.inQ[:, 0, :, 1, :]
        self.outQ[:, 1, :, 0, :] = self.inQ[:, 1, :, 0, :]
        self.outQ[:, 1, :, 1, :] = - self.inQ[:, 1, :, 1, :]

        self.inQ.shape = (-1, self.batchsize)
        self.outQ.shape = (-1, self.batchsize)
        self.inQ, self.outQ = self.outQ, self.inQ

    def cz2(self,q0,q1):
        """ 
        diag(1,1,1,-1)
        """
        qbit0, qbit1 = min(q0, q1), max(q0, q1)
        shape = (2**qbit0, 2, 2**(qbit1 - qbit0 - 1), 2, -1, self.batchsize)
        self.inQ.shape = shape
  
        np.negative(self.inQ[:, 1, :, 1, :], out=self.inQ[:, 1, :, 1, :])

        self.inQ.shape = (-1, self.batchsize)
        
    def measureAll(self):
        return np.abs(self.inQ)**2

SXgate = np.array([[1+1j, 1-1j], [1-1j, 1+1j]], dtype=np.csingle)/2

