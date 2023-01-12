import numpy as np
from test_oqsym import oqsym_run
from time import perf_counter

import sys

depth = 1

for nbqubits in range(24, 25,1):
    params= np.random.rand(depth,nbqubits)
    before = perf_counter()
    oqsym_run(params)
    print(f"{nbqubits}:{perf_counter()-before}s")
    