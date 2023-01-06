import numpy as np
from time import perf_counter

a = np.random.rand(4096,4096)
b = np.random.rand(4096,4096)
A=a+b*1j
a = np.random.rand(4096,4096)
b = np.random.rand(4096,4096)
B=a+b*1j

# print(10*'-')
# A.dot(B)
print(10*'-')

start_time = perf_counter()

# A.dot(B)
np.tensordot(A,B,(1,0))

end_time = perf_counter()

print(f'perf_counter: {end_time- start_time: 0.2f}s')


