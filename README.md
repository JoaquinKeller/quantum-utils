## Quantum utils doc

### installing qiskit with conda-forge

```
conda install pip-tools ply  mpmath  charset-normalizer  websockets  websocket-client  urllib3  sympy  symengine  six  pycparser  psutil  pbr  numpy  ntlm-auth  idna  dill  stevedore  scipy  rustworkx  requests  python-dateutil  cffi  cryptography symengine

pip install qiskit
```

To maintain some consistency in the packages, the idea is to install the dependencies from conda-forge (and not from pip). The rule to enforce is "do not install with pip if you can install with conda"
