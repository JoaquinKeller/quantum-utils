"""
check the output of oqsim 
against the reference (qiskit) 
on random circuits of several sizes
"""

import oqsim

from test_oq import test_oq
if __name__=='__main__':
    test_oq(oqsim.QuantumRegister)            
