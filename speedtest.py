import sys
import numpy as np
from time import perf_counter

from circuit import pcircuit_run, batch_run

def speedtest(simulator, nbqubits, depth, batchsize):       
    if simulator == "qiskit": from qiskitsim import QuantumRegister
    elif simulator == "oqsim": from oqsim import QuantumRegister
    elif simulator == "oqmany": from oqmany import QuantumRegister 
    
    before = perf_counter()
    if batchsize==1:
        params= np.pi* np.random.rand(depth,nbqubits)
        pcircuit_run(params, QR=QuantumRegister) #type:ignore
    else:
        params= np.pi* np.random.rand(depth,nbqubits, batchsize)
        batch_run(params, QR=QuantumRegister)  #type:ignore
        
    totaltime=perf_counter()-before
    return totaltime

if __name__=='__main__':
    depth = nbcircuits= 1
    try:
        simulator=sys.argv[1]
        nbqubits=int(sys.argv[2])
        try:depth=int(sys.argv[3])
        except:pass
        try:nbcircuits=int(sys.argv[4])
        except:pass
    except:
        print(f"usage: python {sys.argv[0]} (qiskit|oqsim) nbqubits [depth [nbcircuits]]")   
        print(f"example: python {sys.argv[0]} oqsim 14 1 1000")   
        print(f"example: python {sys.argv[0]} qiskit 14")   
        sys.exit(0) 

    if simulator not in {"qiskit","oqsim","oqmany"}:
        print(f"Simulator '{simulator}' not available. Available simulators: 'qiskit' 'oqsim' 'oqmany')")
        sys.exit(0)

    print(f"speedtest for {simulator} with nbqubits:{nbqubits} - depth:{depth} - nbcircuits:{nbcircuits}")

    totaltime = speedtest(simulator, nbqubits, depth,nbcircuits)
    
    print(f"total time:{totaltime:.2f}s")
    print(f"time per circuit:{totaltime/nbcircuits:.2f}s\nin milliseconds {1000*totaltime/nbcircuits:.2f}ms ")
        