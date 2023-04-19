import oqmany


class Qcircuit:
    valid_tokens = {'sx', 'cz', 'rz','r'}

    def __init__(self, s: str) -> None:
        self.code = s
        self.parsed = self._parse(s)

    def _parse(self, s: str) -> list[list[str | list]]:
        self.nbparams = 0
        self.highestqubit = 0
        s = s.replace(' ', '')
        s = s.replace('\n', '')
        gates: list = s.split(')')[:-1]
        gates = [gate.split('(') for gate in gates]
        parsed = []
        for gate in gates:
            tok: str = gate[0]
            args: list[str | int] = []
            for e in gate[1].split(','):
                if e == 't':
                    args.append('t')
                    self.nbparams += 1
                else:
                    qubit = int(e)
                    args.append(qubit)
                    self.highestqubit = max(self.highestqubit, qubit)
            parsed.append([tok, args])
        return parsed

    def run_permutation(self, permutation, xparams, lparams, QR=oqmany.QuantumRegister):
        assert len(permutation) == self.nbparams, f"""
        The length of permutation={len(permutation)} does not match 
        the nb of parameters={self.nbparams} of the circuit"""

        assert len(xparams) + len(lparams) == self.nbparams, f"""
        {len(xparams)+ len(lparams)} parameters provided vs {self.nbparams} needed"""

        batchsize = xparams.shape[-1]
        # print(f"batchsize:{batchsize}")
        qr = QR(self.highestqubit+1, batchsize)

        lparams_index = 0
        permutation_index = 0

        for gate in self.parsed:
            tok = gate[0]
            assert tok in self.__class__.valid_tokens, f"{tok} not a valid token"
            args = gate[1]
            run_gate = getattr(qr, tok)
            run_args = []
            for arg in args:
                if type(arg) == int:
                    run_args.append(arg)
                elif arg == 't':
                    param_id = permutation[permutation_index]
                    permutation_index += 1
                    if param_id == -1:
                        run_args.append(lparams[lparams_index])
                        lparams_index += 1
                    else:
                        assert type(param_id) == int, f"{param_id}"
                        run_args.append(xparams[param_id])
            # print(f" tok:{tok}\n run_args:{run_args}")
            run_gate(*run_args)
        return qr.measureAll()

    def _print(self):
        print(f"  nbqubits={1+self.highestqubit}  nbparams={self.nbparams}")
        print(self.parsed)


if __name__ == '__main__':
    import numpy as np


    A2q2t = '''
    sx(0)rz(0,t)sx(0)
    sx(1)rz(1,t)sx(1)
    '''


    qcA2q2t = Qcircuit(A2q2t+"cz(0,1)")
    qcA2q2t._print()
    permutation = [0, -1]
    xparams = np.random.rand(1, 4)
    lparams = np.random.rand(1)
    qcA2q2t.run_permutation(permutation, xparams, lparams)
