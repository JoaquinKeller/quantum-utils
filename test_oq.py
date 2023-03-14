
import numpy as np
import circuit
import qiskitsim


def test_oq(QR, batchsize=None):
    assert batchsize==None or batchsize>=1
    print('Testing',QR.__module__)
    nb_circuits=0
    for nbqubits in range(2,10,1):
        print(30*'-')
        print("nbqubits=",nbqubits)
        for depth in range(1,6,1):
            print("depth=",depth,end='')
            for _ in range(10):
                if batchsize==None:
                   params= np.pi* np.random.rand(depth,nbqubits)
                   c_run= circuit.pcircuit_run
                else:
                   params= np.pi* np.random.rand(depth,nbqubits, batchsize)
                   c_run= circuit.batch_run
                    
                assert np.allclose(c_run(params,QR=QR), #type:ignore  
                                   c_run(params, QR=qiskitsim.QuantumRegister)) #type:ignore              
                nb_circuits+=1
                print('.',end='')
            print()
    print(40*'-')
    print('Tested:',QR.__module__)
    print(f"{nb_circuits} circuits tested with success")     
    
    
if __name__=='__main__':
    test_oq()    
            
