import numpy as np
from time import perf_counter

nbqubit=31
loops=6
print(f"nbqubit:{nbqubit}, loops:{loops}")
CZ_matrix = np.diag([1,1,1,-1])
CZ_tensor = np.reshape(CZ_matrix, (2, 2, 2, 2))
qstate = np.zeros((2,)*nbqubit, dtype=np.csingle)
qstate[(0,)*nbqubit] = 1

before = perf_counter()
for _ in range(loops):
    q0,q1=np.random.randint(0,nbqubit),np.random.randint(0,nbqubit)
    while q0==q1:
        q1=np.random.randint(0,nbqubit)
    qstate=np.tensordot(CZ_tensor, qstate, ((2,3),(q0, q1)))
    qstate=np.moveaxis(qstate,(0,1),(q0,q1))

after = perf_counter()
print("step",after-before)