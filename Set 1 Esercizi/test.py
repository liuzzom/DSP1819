import numpy as np

def mcd(a, b):
    """Restituisce il Massimo Comune Divisore tra a e b"""
    while b:
        a, b = b, a%b
    return a

p = np.array([[7], [4], [11]])
key = np.array([[2, 1, 13], [19, 1, 21], [8, 20, 25]])
print(np.linalg.det(np.array([[1, 13], [20, 25]])))
