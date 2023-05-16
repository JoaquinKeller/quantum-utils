from collections.abc import Iterable
from typing import Optional
import random

from collections import deque

from qcircuit import Qcircuit
import latexqcircuit

class CircuitGenerator:
    FALCON27_TOPOLOGY={(0,1),(1,4),(4,7),(6,7),(7,10),(10,12),(12,13),
                       (13,14),(12,15),(15,18),(17,18),(18,21),(21,23),(23,24),(24,25),(25,26),
                       (1,2),(2,3),(3,5),(5,8),(8,9),(8,11),(11,14),(14,16),(16,19),(19,20),(19,22),(22,25)}
    """ with r and cz """
    def __init__(self, topology:Iterable[tuple[int,int]]) -> None:
        self.topology:set[tuple[int,int]]=set()
        e:tuple[int,int]
        self.nbqubits:int=0
        for q0,q1 in topology:
            assert q0!=q1
            assert q0>=0 and q1>=0
            self.nbqubits=max(self.nbqubits,q0,q1)
            if q0>q1: e=(q1,q0)
            else: e=(q0,q1)
            self.topology.add(e)
        self.nbqubits+=1
            
        
    def greedygenerator(self, nbparams:int, randomseed:Optional[int]=None)->str:
        """Minimize circuit depth"""
        random.seed(randomseed)
        circuit:list[list[str|int]]=[[] for _ in range(self.nbqubits)]
        nbp:int=0
        while nbp<nbparams:
            tangles=set(self.topology)
            while tangles and nbp<nbparams:
                q0,q1=random.choice(tuple(tangles))
                # for line in circuit: line.append('')
                # circuit[q0].append('r')
                # circuit[q1].append('r')
                # circuit[q0].append(q1)
                # circuit[q1].append(q0)
                # circuit[q0].append('r')
                # circuit[q1].append('r')
                for line in circuit: line.append('')
                circuit[q0][-1] ='r'
                circuit[q1][-1] ='r'
                for line in circuit: line.append('')
                circuit[q0][-1]=q1
                circuit[q1][-1]=q0
                for line in circuit: line.append('')
                circuit[q0][-1] ='r'
                circuit[q1][-1] ='r'
                nbp+=4
                tangles.remove((q0,q1))
        
        s:str=''
        for i in range(len(circuit[0])):
            for q in range(self.nbqubits-1,-1,-1):
                try: circuit[q][i]
                except: continue
                if not circuit[q][i]: continue
                if isinstance((circuit[q][i]),int):
                    q1:int=circuit[q][i] #type: ignore
                    if q1<q: continue
                    s=f"\ncz({q},{q1})\n"+s
                elif circuit[q][i]=='r':
                    s=f"r({q},t)"+s
        return s
        

if __name__=='__main__':
    import sys
    c = CircuitGenerator(CircuitGenerator.FALCON27_TOPOLOGY)
    s= c.greedygenerator(200, randomseed=42)
    # print(s) 
    lq  = latexqcircuit.LatexQcircuit(s)
    latexdocument = lq.genlatex(permutation=list(range(lq.nbparams)), 
                                dim=4)
    # sys.exit(0)
    name="IBMqFalcon27_784params"
    name='test'
    with open(f'tex/{name}.tex','w') as f: f.write(latexdocument)
    
    latexqcircuit.latex2pdf(name+'.tex')
    