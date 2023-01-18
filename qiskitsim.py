import qiskit 
import qiskit.quantum_info as qiskit_quantum_info

class QuantumRegister:
    def __init__(self,nbqubit:int) -> None:
        self.nbqubit = nbqubit
        self.qc=qiskit.QuantumCircuit(nbqubit)
    
    def rz(self,q:int,theta:float):
        self.qc.rz(theta,self.nbqubit-1-q)
        
    def sx(self,q:int):
        self.qc.sx(self.nbqubit-1-q)
        
    def cz(self,q0,q1):
        self.qc.cz(self.nbqubit-1-q0,self.nbqubit-1-q1)
        
    def measureAll(self):
        return qiskit_quantum_info.Statevector.from_instruction(self.qc).probabilities()
    
        
