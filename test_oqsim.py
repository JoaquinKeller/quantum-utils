import numpy as np
import circuit_qiskit, circuit_oqsim




if __name__=='__main__':
    nb_tests=0
    for nbqubits in range(2,10,1):
        print(30*'-')
        print("nbqubits=",nbqubits)
        for depth in range(1,6,1):
            print("depth=",depth,end='')
            for _ in range(10):
                params= np.random.rand(depth,nbqubits)
                assert np.allclose( circuit_qiskit.pcircuit_run(params), circuit_oqsim.pcircuit_run(params))
                nb_tests+=1
                print('.',end='')
            print()
    print(40*'-')
    print(f"{nb_tests} tests passed with success")         
            
