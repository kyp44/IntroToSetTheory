"""
Calculates weak Goodstein sequence from
given base (first argument). Does N (second
argument) iterations. If no N is passed
that runs until termination.
"""
from pylab import *
import sys

m = int(sys.argv[1])
N = (int(sys.argv[2]) if len(sys.argv) > 2 else None)

def base(n, b):
    """
    Converts a natural number n to base b.
    Returns list of tuples where the first
    element is the exponent of b and the 
    is the coefficient of that term (the
    digit less than b). Only nonzero
    digits are returns.
    """
    if n == 0:
        return [0]
    ret = []
    while True :
        e = int(log(n)/log(b))
        d = int(n / b**e)
        ret.append((e, d))
        n = n % (b**e * d)
        if e == 0 or n == 0:
            break

    return ret

k = 0
while True :
    ed = base(m, k+2)
    print(k, m, ed)

    if m == 0 or (N != None and k == N) :
        break

    m = sum([(k+3)**e * d for e,d in ed]) - 1
    k += 1
        
