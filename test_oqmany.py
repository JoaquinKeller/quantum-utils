"""
check the output of oqmany 
against the reference (qiskit) 
on random circuits of several sizes
"""

import oqmany

from test_oq import test_oq
if __name__=='__main__':
    test_oq(oqmany.QuantumRegister)            
