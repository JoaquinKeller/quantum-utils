from qcircuit import Qcircuit
from string import Template

LATEX_DOCUMENT_TEMPLATE = r"""\documentclass[preview]{standalone}
\usepackage[letterpaper,margin=2cm,landscape]{geometry}
\usepackage{graphicx}
\usepackage[dvipsnames]{xcolor}
\usepackage{amssymb}
\usepackage{MnSymbol}
\usepackage{adjustbox}

\usepackage[braket]{qcircuit}
%\renewcommand{\familydefault}{\sfdefault}

\newcommand{\losange}{\hspace{0.8em}\lozenge&&}
\newcommand{\ketzero}{\ket{0}&&}
\newcommand{\ketone}{\ket{1}&&}
\newcommand{\ketplus}{\ket{+}&&}
\newcommand{\ketminus}{\ket{-}&&}
\newcommand{\qdots}{\dots&&}
\newcommand{\xygate}[1]{\measure{\!\scriptscriptstyle{#1}\!}}
\newcommand{\zzgate}{\gate{\!{\scriptscriptstyle{z}\!}}}

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
    else: indexs = f"_{index}"
    return r"{\color{MidnightBlue}\theta%s}"%indexs

def xparam2latex(index:int)->str:
    indexs:str = f"_{index}"
    return "{\\color{{MidnightBlue}}\\omega%s}}"%indexs
    


class LatexQcircuit(Qcircuit):
    def __init__(self, s: str) -> None:
        super().__init__(s)
        nbqubits = self.highestqubit+1
        self.visualcircuit= [[] for _ in range(nbqubits)]
        self.latexqubits = ["" for _ in range(nbqubits)]
        for gate in self.parsed:
            self.appendgate(gate)
        self.compact()
        
    def appendgate(self,gate:list)->None:
        tok=gate[0]
        q0 = gate[1][0]
        if tok in self.__class__.entangling_tokens:
            q1 = gate[1][1]
            assert q0<q1
            for q in range(len(self.visualcircuit)):
                if q == q0: self.visualcircuit[q].append([gate[0],gate[1][1:]])
                elif q == q1: self.visualcircuit[q].append(['ctrl',gate[1][2:]])
                else: self.visualcircuit[q].append([])
        else:
            for q in range(len(self.visualcircuit)):
                if q==q0: self.visualcircuit[q].append([gate[0],gate[1][1:]])
                else:  self.visualcircuit[q].append([])
    
    def compact(self):
        haschanged=True
        while haschanged:
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
                        if not self.visualcircuit[otherqubit][i]:
                            otherline = self.visualcircuit[otherqubit]
                            print(otherline)
                            assert self.visualcircuit[otherqubit][i+1][0]=='ctrl'
                            line[i],line[i+1]=line[i+1],line[i]
                            otherline[i],otherline[i+1]=otherline[i+1],otherline[i]
                            haschanged=True
                            print(otherline[i]) 
        # maxdepth = len(self.visualcircuit[0])
        maxdepth = -1
        for line in self.visualcircuit:
            for i in range(len(self.visualcircuit[0])-1, -1, -1):
                if line[i]:
                    maxdepth=max(maxdepth,i)
                    break
                
        for q in range(len(self.visualcircuit)):
            line=self.visualcircuit[q]
            self.visualcircuit[q]=line[:maxdepth+1]
            
            
        
        
                        
        
    
    def genlatex(self, permutation=None)-> str:
        for q in range(len(self.visualcircuit)):
            for gate in self.visualcircuit[q]:
                if gate == []:
                    self.latexqubits[q]+=r"&\qw"
                elif gate[0] == 'r':
                    self.latexqubits[q]+=r"&\gate{"+lparam2latex()+'}'
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
    
    
if __name__=="__main__":
    # lq = LatexQcircuit("r(0)r(1)cz(0,1)r(2)cz(1,2)r(0)r(0)r(0)r(2)cz(0,2)")
    lq = LatexQcircuit(Qcircuit.Afalcon120t)
    latexdocument = lq.genlatex()
    # for qline in lq.visualcircuit: print(qline)
    # for s in lq.latexqubits: print(s)
    with open('tex/test.tex','w') as f:
        f.write(latexdocument)
        