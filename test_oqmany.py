"""
check the output of oqmany 
against the reference (qiskit) 
on random circuits of several sizes
"""

import numpy as np
import circuit
import oqmany,qiskitsim


if __name__=='__main__':
    nb_circuits=0
    for nbqubits in range(2,10,1):
        print(30*'-')
        print("nbqubits=",nbqubits)
        for depth in range(1,6,1):
            print("depth=",depth,end='')
            for _ in range(10):
                params= np.random.rand(depth,nbqubits)
                assert np.allclose(circuit.pcircuit_run(params,QR=oqmany.QuantumRegister), #type:ignore  
                                   circuit.pcircuit_run(params, QR=qiskitsim.QuantumRegister)) #type:ignore              
                nb_circuits+=1
                print('.',end='')
            print()
    print(40*'-')
    print(__doc__)
    print(f"{nb_circuits} circuits tested with success")         
            
