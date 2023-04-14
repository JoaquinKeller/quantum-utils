import numpy as np
import numexpr as ne
from abstractQregister import AbstractQuantumRegister

# self=dict()
class QuantumRegister(AbstractQuantumRegister):
    batchcapable = True
    @staticmethod
    def makeShotsFromProba(proba:np.ndarray, nbshots:int):
        if proba.ndim ==2:
            return np.random.multinomial(nbshots, proba) #type:ignore
        else:
            def fun(v): return np.random.multinomial(nbshots, v)
            return np.apply_along_axis(fun, 0, proba) #type:ignore
 
    
    def __init__(self, nbqubit:int, batchsize:int=1) -> None:
        self.nbqubit = nbqubit
        self.batchsize=batchsize
        self.inQ = np.zeros((2**nbqubit, batchsize), dtype=np.csingle)  # quantum state, input buffer 
        self.outQ = np.empty_like(self.inQ)
        self.proba = None
        self.reset()

    
    def reset(self):
        self.inQ.fill(0)
        self.inQ[0].fill(1)
        self.proba = None
        
    def rz(self, q:int, theta):
        assert q<self.nbqubit
        assert self.batchsize==1 or theta.shape == (self.batchsize,) or np.isscalar(theta)

        if np.isscalar(theta): # à tester
            self.rzscalar(q, theta)
            return

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

    def rzscalar(self, q:int, theta):
        assert q<self.nbqubit
        assert self.batchsize==1 or np.isscalar(theta)
        # t2 = theta/2

        t2 = theta/2
        cost = np.cos(t2)
        isint = 1j*np.sin(t2)
        gate00 = cost - isint
        gate11 = cost + isint

        shape = (2**q, 2, -1, self.batchsize)
        self.inQ.shape = shape
        self.outQ.shape = shape
        q0 = self.inQ[:, 0, :]
        q1 = self.inQ[:, 1, :]
        self.outQ[:, 0, :] = gate00 * q0
        self.outQ[:, 1, :] = gate11 * q1

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
        self.proba = np.abs(self.inQ)**2
        if self.batchsize==1: self.proba = self.proba[:,0]
        return self.proba

    def makeShots(self,nbshots):
        if self.proba is None: self.measureAll()
        return __class__.makeShotsFromProba(self.proba, nbshots) #type:ignore 
    
SXgate = np.array([[1+1j, 1-1j], [1-1j, 1+1j]], dtype=np.csingle)/2

if __name__=='__main__':
    # basic test
    qr = QuantumRegister(2,2)
    qr.sx(0)
    print(qr.measureAll())
    # import oqsim
    # qr = oqsim.QuantumRegister(2)
    # qr.sx(0)
    # print(qr.measureAll())
    

