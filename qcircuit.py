
class Qcircuit:
    def __init__(self, s:str) -> None:
        self.parsed = self._parse(s)
        
    def _parse(self,s:str)->list[list[str|int]]:
        self.nbparams = 0
        self.highestqubit=0
        s = s.replace(' ','')
        s = s.replace('\n','')
        gates:list = s.split(')')[:-1]
        gates = [gate.split('(') for gate in gates]
        parsed = []
        for gate in gates:
            tok:str = gate[0]
            args:list[str|int] = []
            for e in gate[1].split(','):
                if e == 't':
                    args.append('t')
                    self.nbparams+=1
                else:
                    qubit = int(e)
                    args.append(qubit)
                    self.highestqubit = max(self.highestqubit,qubit)
            parsed.append([tok,args])
        return parsed



if __name__=='__main__':
    print(Qcircuit("sx(1)rz(2,t)cz(0,1)").parsed)
    
    A1q2t = '''
    sx(0)rz(0,t)sx(0)
    sx(1)rz(1,t)sx(1)
    '''
    A2q8t = 3*(A1q2t+' cz(0,1)')+A1q2t
    print(A2q8t)
    qcA2q8t = Qcircuit(A2q8t)
    print(f"""
          nbqubits={1+qcA2q8t.highestqubit}
          nbparams={qcA2q8t.nbparams}
          """)
    print(qcA2q8t.parsed)
    