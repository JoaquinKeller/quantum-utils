from qcircuit import Qcircuit
from string import Template

# \usepgfplotslibrary{external} 
# \tikzexternalize


LATEX_DOCUMENT_TEMPLATE = r"""\documentclass[preview]{standalone}
\usepackage[letterpaper,margin=2cm,landscape]{geometry}
\usepackage{graphicx}
\usepackage[dvipsnames]{xcolor}
\usepackage{amssymb}
\usepackage{MnSymbol}
\usepackage{adjustbox}
\usepackage[braket]{qcircuit}
%\renewcommand{\familydefault}{\sfdefault}

\newcommand{\ketzero}{\ket{0}&&}
\newcommand{\qdots}{\dots&&}

\begin{document}
\pagenumbering{gobble}
~ \\
\centering{\huge{$title}}

$qcircuit
\centering{\Large{$caption}}
    
\vspace{\fill}

\end{document}
"""

LATEX_CIRCUIT_TEMPLATE = r""" 
\adjustbox{width=\textwidth, margin={24mm 10mm 15mm 12mm},
max totalsize={\textwidth}{\textheight}, keepaspectratio}
{\Qcircuit @C=0.3em @R=1em {$qqq}}\\
"""

def lparam2latex(index:int=-1)->str:
    indexs:str
    if index<0: indexs=""
    else: indexs = f"_{{{index}}}"
    return r"{\color{JungleGreen}\theta%s}"%indexs

def xparam2latex(index:int, dim:int=0)->str:
    indexs:str 
    if dim: indexs= f"^{{{index%dim}}}_{{{index//dim}}}"
    else: indexs= f"_{{{index}}}"
    color:str = "BrickRed"
    # colortable = ('Magenta','Bittersweet','ForestGreen')
    colortable = ('Magenta','Cerulean','OliveGreen','BurntOrange')
    ncolor=len(colortable)
    if dim:
        color=colortable[(index//dim)%ncolor] 
    # return r"{\color{BrickRed}\omega%s}"%indexs
    return r"{\color{"+color+r"}\theta%s}"%indexs
    


class LatexQcircuit(Qcircuit):
    def __init__(self, s: str) -> None:
        super().__init__(s)
        # print(self.nbparams)
        nbqubits = self.highestqubit+1
        
    def appendgate(self,gate:list, param_id:int=-1, lparam_id:int=-1)->None:
        # print(param_id)
        tok=gate[0]
        q0 = gate[1][0]
        if tok in self.__class__.entangling_tokens:
            q1 = gate[1][1]
            assert q0<q1
            for q in range(len(self.visualcircuit)):
                if q == q0: self.visualcircuit[q].append([gate[0],gate[1][1:]])
                elif q == q1: self.visualcircuit[q].append(['ctrl',gate[1][2:]])
                elif q0 < q <q1: self.visualcircuit[q].append([''])
                else: self.visualcircuit[q].append([])
        else:
            for q in range(len(self.visualcircuit)):
                if q==q0: self.visualcircuit[q].append([gate[0],gate[1][1:],param_id,lparam_id])
                else:  self.visualcircuit[q].append([])
    
    def compact(self, n=9999):
        haschanged=True
        while haschanged and n>0:
            haschanged=False
            for q in range(len(self.visualcircuit)):
                line=self.visualcircuit[q]
                assert len(line) == len(self.visualcircuit[0])
                for i in range(len(line)-1):
                    currentgate = line[i]
                    nextgate = line[i+1]
                    if currentgate or not nextgate: continue
                    if nextgate[0]=='r':
                        line[i],line[i+1]=line[i+1],line[i]
                        haschanged=True
                    elif nextgate[0]=='cz':
                        # print('cz')
                        otherqubit = nextgate[1][0]
                        oktoshift= not self.visualcircuit[otherqubit][i]
                        # for k in range(q+1,otherqubit):
                        #     oktoshift = oktoshift and  not self.visualcircuit[k][i]
                        if oktoshift:
                            for k in range(q,otherqubit+1):
                                l = self.visualcircuit[k]
                                l[i],l[i+1]=l[i+1],l[i]                                
                            otherline = self.visualcircuit[otherqubit]
                            # print(otherline)
                            # assert self.visualcircuit[otherqubit][i+1][0]=='ctrl'
                            # line[i],line[i+1]=line[i+1],line[i]
                            # otherline[i],otherline[i+1]=otherline[i+1],otherline[i]
                            haschanged=True
                            n-=1
                            if n<=0: break
                            # print(otherline[i]) 
        # maxdepth = len(self.visualcircuit[0])
        if n<=0: return
        maxdepth = -1
        for line in self.visualcircuit:
            for i in range(len(self.visualcircuit[0])-1, -1, -1):
                if line[i]:
                    maxdepth=max(maxdepth,i)
                    break
                
        for q in range(len(self.visualcircuit)):
            line=self.visualcircuit[q]
            self.visualcircuit[q]=line[:maxdepth+1]
    
    def __printvisualcircuit(self):
        for line in self.visualcircuit:
            for gate in line:
                if not gate: print("-", end='')
                elif not gate[0]: print("|", end='')
                elif gate[0]=='cz': print("*", end='')
                elif gate[0]=='ctrl': print("!", end='')
                else: print(gate[0], end='') 
            print()
                
    
    def genlatex(self, permutation:list=[], dim:int=0)-> str:
        nbqubits = self.highestqubit+1
        self.visualcircuit= [[] for _ in range(nbqubits)]
        self.latexqubits = ["" for _ in range(nbqubits)]
        if not permutation:
            permutation=self.nbparams*[-1]
        assert len(permutation) == self.nbparams, "permutation lenght is wrong"
        print(len(permutation))
        
        permutation_index=0
        lparam_id=-1
        for gate in self.parsed:
            param_id=-1
            if gate[0]=='r': 
                param_id= permutation[permutation_index]
                permutation_index += 1
                if param_id==-1: lparam_id+=1
            self.appendgate(gate, param_id=param_id, lparam_id=lparam_id)
        self.compact()
        self.__printvisualcircuit()
        permutation_index=0
        for q in range(len(self.visualcircuit)):
            for gate in self.visualcircuit[q]:
                if gate == [] or gate[0]=="":
                    self.latexqubits[q]+=r"&\qw"
                elif gate[0] == 'r':
                    print("permutation_index",permutation_index)
                    param_id = permutation[permutation_index]
                    param_id = gate[2]
                    # print('param_id:',param_id)
                    permutation_index += 1
                    if param_id == -1:
                        lparam_id = gate[3]
                        self.latexqubits[q]+=r"&\gate{"+lparam2latex(lparam_id)+'}'
                    else:
                        assert type(param_id) == int, f"{param_id}"
                        self.latexqubits[q]+=r"&\gate{"+xparam2latex(param_id,dim=dim)+'}'
                        
                elif gate[0] == 'cz':
                    target = gate[1][0]-q
                    self.latexqubits[q]+='&\\ctrl{%s}'%target
                elif gate[0] == 'ctrl':
                    self.latexqubits[q]+=r'&\ctrl{0}'
        latexqcircuit = ""
        for line in self.latexqubits:
            latexqcircuit+="\n"+r"\ketzero"+line+r'&\meter\\'
        latexqcircuit = Template(LATEX_CIRCUIT_TEMPLATE).substitute(qqq=latexqcircuit)
        
        return Template(LATEX_DOCUMENT_TEMPLATE
                        ).substitute(title='',
                                     qcircuit=latexqcircuit,
                                     caption='')

import subprocess,os

def latex2pdf(name='test.tex',texdir='tex/'):

    wd = os.getcwd()
    os.chdir(texdir)

    # cmd = ['pdflatex', '--halt-on-error', '--interaction=nonstopmode','-shell-escape', name]
    cmd = ['pdflatex', '--halt-on-error', '--interaction=nonstopmode','--enable-write18', name]
    cmd = ['pdflatex', '--halt-on-error','--interaction=nonstopmode', name]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    p.wait()
    if not not p.returncode: 
        errormsg = ""
        lines = p.stdout if p.stdout else ["unknown error".encode()]
        for line in lines:
            errormsg+=line.decode('utf-8')
        raise Exception(errormsg+"\nLatex generation failed for "+name)
    os.chdir(wd)
    
if __name__=="__main__":
    # lq = LatexQcircuit("r(0,t)r(1,t)cz(0,1)r(1,t)r(2,t)cz(1,2)r(0,t)r(1,t)r(1,t)r(2,t)cz(0,3)r(0,t)cz(0,2)")
    lq = LatexQcircuit("""r(0,t)r(1,t)r(2,t)r(3,t)
r(4,t)r(5,t)r(6,t)
cz(1,2)cz(4,5)
    r(1,t)r(2,t)r(4,t)r(5,t)
    cz(0,1)cz(3,5)
    r(0,t)r(1,t)r(3,t)r(5,t)
    cz(1,3)cz(5,6)
    r(1,t)r(3,t)r(5,t)r(6,t)"""
        
    )
    # lq = LatexQcircuit(Qcircuit.Bfalcon120t)  
    # latexdocument = lq.genlatex(permutation=list(range(lq.nbparams)), dim=4)
    latexdocument = lq.genlatex(permutation=[-1, 8, 9, -1, 3, 4, 10, 5, 1, -1, 6, -1, 0, -1,  -1, 7, -1, 11, 2], dim=12)
    # latexdocument = lq.genlatex(dim=4)
    # for qline in lq.visualcircuit: print(qline)
    # for s in lq.latexqubits: print(s)
    with open('tex/test.tex','w') as f: f.write(latexdocument)

    # latex2pdf() 
        