import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pickle
import os.path
import numpy as np
from math import sqrt, log2

from geometric import firstgeometric, firstgeometricsimple, moregeometric
from ourscheme import make_kaiburr_scheme, target_params

Grover = lambda alpha, MaxDepth: (alpha**0.5) * max(1, alpha**0.5/MaxDepth)

f_alpha = [u'work to generate one weak sample (1/α)', lambda a, b: a]
f_sqrtalpha = [u'work to generate one weak sample (1/√α)', lambda a,b: sqrt(a)]
f_beta = [u'weak ciphertext failure rate (β)', lambda a,b: b]
f_alphabeta = [u'total work to generate a failure (1/αβ)', lambda a, b: a * b**-1]
f_sqrtalphabeta = [u'total work to generate a failure (1/β√α)', lambda a, b: sqrt(a) * b**-1]

f_sqrtalphabetagrover = [u'total work to generate a failure (1/β√α)', lambda a, b, maxdepth: Grover(a, maxdepth) * b**-1]
f_sqrtalpha = [u'work to generate one weak sample (1/√α)', lambda a, b, maxdepth: Grover(a, maxdepth)]

def failureboosting(scheme, method, n_failure, recalc=False, targets=1, beta0=None):
    n = scheme['n']
    n2 = scheme['n2']
    thres = scheme['thres']
    s = scheme['s']
    sprime = scheme['sprime']
    e = scheme['e']
    eprime = scheme['eprime']
    eprimeprime = scheme['eprimeprime']

    extraname = ""
    if targets > 1 or beta0 != None:
        extraname = f"-T{targets}-beta{int(round(np.log2(beta0)))}"
    name = 'intermediates_fb/'+scheme['name'] + '-' + method + '-' + str(n_failure) + extraname

    if os.path.exists(name + '-' + 'beta.txt') and not recalc:
        alpha = np.loadtxt(name + '-' + 'alpha.txt')
        beta = np.loadtxt(name + '-' + 'beta.txt')
    else:
        if method == 'geometric':
            if n_failure == 1:
                alpha, beta = firstgeometric(n, n2, thres, s, sprime, e, eprime, eprimeprime)
            else:
                alpha, beta = moregeometric(n, n2, thres, s, sprime, e, eprime, eprimeprime, n_failure, targets=targets, beta0=beta0)
        elif method == 'geometric-simple':
            if n_failure == 1:
                alpha, beta = firstgeometricsimple(n, n2, thres, s, sprime, e, eprime, eprimeprime)
        else:
            raise Exception('not a valid method')

        np.savetxt(name + '-' + 'alpha.txt', alpha)
        np.savetxt(name + '-' + 'beta.txt', beta)

    return alpha, beta

if __name__ == "__main__":
    for m, n, q in target_params:
        scheme = make_kaiburr_scheme(m, n, q)
        alpha, beta = failureboosting(scheme, 'geometric', 1)
        costs = [sqrt(a) * b**-1 for a, b in zip(alpha, beta) if b > 0]
        print(f"m={m}, n={n}, q={q}: fb cost = 2^{log2(min(costs)):.1f}")