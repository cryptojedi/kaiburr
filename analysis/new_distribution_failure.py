from distribution import sample_f

import operator as op
from math import factorial as fac
from math import sqrt, log
import sys
from proba_util import *

def build_exact_distribution(n):
    """exact probability law for f(n)"""
    return {
        0:  0.5 - 0.5**(n-1),
        1:  0.25,
        -1: 0.25,
        2:  0.5**n,
        -2: 0.5**n,
    }

def build_limiting_distribution():
    """the limiting distribution as n goes to infinity;
     probability of getting +-2 approaches 0 and the distribution concentrates on {-1, 0, 1}"""
    return {
        0:  0.5,
        1:  0.25,
        -1: 0.25,
        2:  0.0,
        -2: 0.0,
    }

def _noise_law(ps, param):
    """ noise law for a f(n) param or a centered binomial law if ps.cbd is set
    """
    cbd = getattr(ps, "cbd", None)
    if cbd is not None:
        return build_centered_binomial_law(cbd)
    return build_exact_distribution(param)


def p2_cyclotomic_final_error_distribution(ps):
    """ construct the final error distribution in our encryption scheme
    :param ps: parameter set (ParameterSet)
    """
    chis = _noise_law(ps, ps.ks)           # LWE error law for the key
    chie = _noise_law(ps, ps.ke_ct)        # LWE error law for the ciphertext
    chie_pk = _noise_law(ps, ps.ke)
    Rk = build_mod_switching_error_law(ps.q, ps.rqk)    # Rounding error public key
    Rc = build_mod_switching_error_law(ps.q, ps.rqc)    # rounding error first ciphertext
    chiRs = law_convolution(chis, Rk)                   # LWE+Rounding error key
    chiRe = law_convolution(chie, Rc)                   # LWE + rounding error ciphertext

    B1 = law_product(chie_pk, chiRs)                       # (LWE+Rounding error) * LWE (as in a E*S product)
    B2 = law_product(chis, chiRe)

    C1 = iter_law_convolution(B1, ps.m * ps.n)
    C2 = iter_law_convolution(B2, ps.m * ps.n)

    C=law_convolution(C1, C2)

    R2 = build_mod_switching_error_law(ps.q, ps.rq2)    # Rounding2 (in the ciphertext mask part)
    F = law_convolution(R2, chie)                       # LWE+Rounding2 error
    D = law_convolution(C, F)                           # Final error
    return D


def p2_cyclotomic_error_probability(ps):
    """
    compute the decryption failure probability
    recall: failure occurs when the decryption error exceeds q/4 in absolute value,
    so failure probability is the tail probability of the error distribution beyond q/4,
    multiplied by n
    """
    F = p2_cyclotomic_final_error_distribution(ps)
    proba = tail_probability(F, ps.q/4)
    return F, ps.n*proba