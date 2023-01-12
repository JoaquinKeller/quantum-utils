import numpy as np
import sys
import oqsym

import qiskit 

def oqsym_run(params):
    nbqubits=params.shape[1]
    
    qc=oqsym.QuantumRegister(nbqubits)
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

def qiskit_run(params):
    nbqubits=params.shape[1]
    qc=qiskit.QuantumCircuit(nbqubits)
    for step in params:
        for qubit,v in enumerate(step):
            qc.sx(nbqubits-1-qubit)
            qc.rz(v,nbqubits-1-qubit)
            qc.sx(nbqubits-1-qubit)
        for qubit in range(nbqubits-1):
            qc.cz(nbqubits-1-qubit,nbqubits-1-qubit-1)
    for qubit in range(nbqubits):
        qc.sx(qubit)
    return qiskit.quantum_info.Statevector.from_instruction(qc).probabilities()


if __name__=='__main__':
    # depth = 2
    # nbqubits=3
    # params= np.random.rand(depth,nbqubits)
    # comparewithqiskit(params)
    # sys.exit(0)
    
    nb_tests=0
    for nbqubits in range(2,10,1):
        print(30*'-')
        print("nbqubits=",nbqubits)
        for depth in range(1,6,1):
            print("depth=",depth,end='')
            for _ in range(10):
                params= np.random.rand(depth,nbqubits)
                assert np.allclose( qiskit_run(params), oqsym_run(params))
                nb_tests+=1
                print('.',end='')
            print()
    print(40*'-')
    print(f"{nb_tests} tests passed with success")         
            

    # print(comparewithqiskit(params))

    sys.exit(0)
    print(qiskit_run(params))
    circ = qiskit.QuantumCircuit(2)
    circ.h(0)
    circ.cx(0, 1)
    
    
    
    stv1 = qi.Statevector.from_instruction(circ)
    # circ.measure_all()


    # Transpile for simulator
    # simulator = qiskit.Aer.get_backend('aer_simulator')
    # circ = qiskit.transpile(circ, simulator)

    # Run and get counts
    # result = simulator.run(circ, method='statevector', statevector=True).result()
    # statevector = result.get_statevector(circ)
    
    # print(dir(result))
    # print(result.data(0))
    # print(dir(stv1))
    print(stv1.to_dict())
    print(stv1.probabilities())