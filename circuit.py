import oqsim
from abstractQregister import AbstractQuantumRegister


def pcircuit_run(params,QR=oqsim.QuantumRegister):
    assert params.ndim==2
    nbqubits=params.shape[1]
    batchsize=1
    
    qc=QR(nbqubits,batchsize)
    for step in params:
        for qubit,v in enumerate(step):
            qc.sx(qubit)
            qc.rz(qubit,v)
            qc.sx(qubit)
        for qubit in range(nbqubits-1):
            qc.cz(qubit,qubit+1)
    for qubit in range(nbqubits):
        qc.sx(qubit)
    return qc.measureAll()
