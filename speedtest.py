import sys
import numpy as np
from time import perf_counter

from circuit import pcircuit_run

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

if simulator == "qiskit": from qiskitsim import QuantumRegister
elif simulator == "oqsim": from oqsim import QuantumRegister
else:
    print(f"Simulator '{simulator}' not available. Available simulators: 'qiskit' 'oqsim')")
    sys.exit(0)
    
def run_pcircuit(params):
    pcircuit_run(params,QR=QuantumRegister) #type:ignore


print(f"nbqubits:{nbqubits} - depth:{depth} - nbcircuits:{nbcircuits}")

before = perf_counter()
for _ in range(nbcircuits):
    params= np.random.rand(depth,nbqubits)
    run_pcircuit(params) 
totaltime=perf_counter()-before
print(f"total time:{totaltime}s")
if nbcircuits>1: print(f"time per circuit:{totaltime/nbcircuits}s")
    