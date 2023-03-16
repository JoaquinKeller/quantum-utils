
import numpy as np
import circuit
import qiskitsim


def test_oq(QR, batchsize=None):
    assert batchsize==None or batchsize>=1
    nb_circuits=0
    for nbqubits in range(2,10,1):
        for depth in range(1,4,1):
            for _ in range(5):
                if batchsize==None:
                    params= np.pi* np.random.rand(depth,nbqubits)
                    c_run= circuit.pcircuit_run
                else:
                    params= np.pi* np.random.rand(depth,nbqubits, batchsize)
                    c_run= circuit.batch_run
                assert np.allclose( c_run(params,QR=QR), #type:ignore  
                                    c_run(params, QR=qiskitsim.QuantumRegister)) #type:ignore              
                nb_circuits+=1
    print(QR.__module__,':  ', end='')
    if batchsize==None:
        print(f"{nb_circuits} random circuits tested with success")   
    else:
        print(f"{nb_circuits} batches of {batchsize} random circuits tested with success")   

if __name__=='__main__':
    import oqsim, oqmany
    test_oq(oqsim.QuantumRegister)     
    test_oq(oqmany.QuantumRegister)            
    for batchsize in range(1,5,1):
        test_oq(oqsim.QuantumRegister,batchsize)     
        test_oq(oqmany.QuantumRegister,batchsize)            

    print("\noqsim and oqmany: successfully and fully tested against qiskit\n")   
    
            
