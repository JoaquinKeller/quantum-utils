
import qiskit 
import qiskit.quantum_info as qiskit_quantum_info

def pcircuit_run(params):
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
    return qiskit_quantum_info.Statevector.from_instruction(qc).probabilities()