import oqsim, oqmany
from abstractQregister import AbstractQuantumRegister
import numpy as np


def pcircuit_run(params,QR=oqsim.QuantumRegister, batchsize=1):
    assert (params.ndim==2 and batchsize==1) or (batchsize>1 and QR.batchcapable and params.ndim==3) 
    nbqubits=params.shape[1]
    
    qc=QR(nbqubits,batchsize)
    for step in params:
        for qubit,theta in enumerate(step):
            qc.sx(qubit)
            qc.rz(qubit,theta)
            qc.sx(qubit)
        for qubit in range(nbqubits-1):
            qc.cz(qubit,qubit+1)
    for qubit in range(nbqubits):
        qc.sx(qubit)
    return qc.measureAll()

def batch_run(params, circuit_run=pcircuit_run, QR=oqmany.QuantumRegister):
    assert params.ndim>=2
    if params.ndim==2: batchsize=1
    else: 
        batchsize=params.shape[2]
        if batchsize==1: params=params[:,:,0]
    if batchsize>1 and not QR.batchcapable:
        batchresult = np.zeros(batchsize,dtype=float)
        for i in range(batchsize):
            batchresult[i]=circuit_run(params[:,:,i], QR=QR) #type:ignore
        return batchresult
    return circuit_run(params, QR=QR, batchsize=batchsize) #type:ignore
    

if __name__=='__main__':
    import numpy as np
    depth, nbqubits, batchsize = 3,7,1
    params = np.pi * np.random.rand(depth, nbqubits, batchsize)
    # pcircuit_run(params, QR=oqsim.QuantumRegister)  #type:ignore  
    params= np.random.rand(depth,nbqubits)
                # assert np.allclose(circuit.pcircuit_run(params,QR=oqmany.QuantumRegister),
    pcircuit_run(params, QR=oqmany.QuantumRegister, batchsize=batchsize)  #type:ignore  