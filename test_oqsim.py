"""
check the output of oqsim 
against the reference (qiskit) 
on random circuits of several sizes
"""

import numpy as np
import circuit_qiskit, circuit_oqsim



if __name__=='__main__':
    nb_circuits=0
    for nbqubits in range(2,10,1):
        print(30*'-')
        print("nbqubits=",nbqubits)
        for depth in range(1,6,1):
            print("depth=",depth,end='')
            for _ in range(10):
                params= np.random.rand(depth,nbqubits)
                assert np.allclose( circuit_qiskit.pcircuit_run(params), circuit_oqsim.pcircuit_run(params))
                nb_circuits+=1
                print('.',end='')
            print()
    print(40*'-')
    print(__doc__)
    print(f"{nb_circuits} circuits tested with success")         
            
