import numpy as np
from time import perf_counter

import sys

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

if simulator == "qiskit": from circuit_qiskit import pcircuit_run
elif simulator == "oqsim": from circuit_oqsim import pcircuit_run
else:
    print(f"Simulator {simulator} not available")
    sys.exit(0)

print(f"nbqubits:{nbqubits} - depth:{depth} - nbcircuits:{nbcircuits}")

before = perf_counter()
for _ in range(nbcircuits):
    params= np.random.rand(depth,nbqubits)
    pcircuit_run(params)
totaltime=perf_counter()-before
print(f"total time:{totaltime}s")
if nbcircuits>1: print(f"time per circuit:{totaltime/nbcircuits}s")
    