
import qiskit 
import qiskit.quantum_info as qiskit_quantum_info

def pcircuit_run(params):
    nbqubit=params.shape[1]
    qc=qiskit.QuantumCircuit(nbqubit)
    for step in params:
        for q,theta in enumerate(step):
            qc.sx(nbqubit-1-q)
            qc.rz(theta,nbqubit-1-q)
            qc.sx(nbqubit-1-q)
        for q in range(nbqubit-1):
            qc.cz(nbqubit-1-q,nbqubit-1-q-1)
    for q in range(nbqubit):
        qc.sx(q)
    return qiskit_quantum_info.Statevector.from_instruction(qc).probabilities()