from math import sqrt, log, log2, ceil
from scipy.special import erf
from new_distribution_failure import p2_cyclotomic_error_probability
from kaiburr import KyberParameterSet

def variance_f(n):
    """
    computes variance of one coefficient from f(n)"""
    return 0.5 + 2**(3-n)

## probability mass function for f(n)
def f_n(i, n):
    if i == 0: return 0.5 - 0.5**(n-1)
    elif abs(i) == 1: return 0.25
    elif abs(i) == 2: return 0.5**n
    else: return 0

def get_failure_exp(m, n, q=3329, rqk=None, rqc=None, rq2=None):
    if rqk is None: rqk = 2**ceil(log2(q + 1))
    if rqc is None: rqc = 2**ceil(log2(q + 1))
    if rq2 is None: rq2 = 2**ceil(log2(q + 1))
    ps = KyberParameterSet(256, m, n, n, q, rqk, rqc, rq2)
    F, f = p2_cyclotomic_error_probability(ps)
    return log(f + 2.**(-300)) / log(2)

def expected_pm2(n, m, poly_degree=256):
    """ computes the expected number of ±2 coefficients across ALL polynomials"""
    return (4*m + 1) * poly_degree * 2 * 0.5**n

def n_star_formula(m, epsilon=1.0, poly_degree=256):
    """ computes the theoretical threshold; minimum n at which failure probability plateaus"""
    return ceil(log2((4*m + 1) * poly_degree * 2 / epsilon))

def find_min_n(m, q, threshold=-128):
    for n in range(4, 100):
        fail = get_failure_exp(m, n, q)
        if fail <= threshold:
            return n, fail
    return None, None