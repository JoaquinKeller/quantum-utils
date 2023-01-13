import oqsim

def pcircuit_run(params):
    nbqubits=params.shape[1]
    
    qc=oqsim.QuantumRegister(nbqubits)
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
