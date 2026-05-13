from dist import Dist
from math import sqrt, ceil, log2

import sys
sys.path.append('..')
from new_distribution_failure import build_exact_distribution
from proba_util import build_mod_switching_error_law

def make_kaiburr_scheme(m, n, q, rq2):
    rqk = 2**ceil(log2(q + 1))
    base = Dist(build_exact_distribution(n))
    u_ct = Dist(build_mod_switching_error_law(q, rqk))
    u2   = Dist(build_mod_switching_error_law(q, rq2))

    scheme = {}
    scheme['name']        = f'm{m}_n{n}_q{q}_rq2_{rq2}'
    scheme['thres']       = q / 4
    scheme['s']           = base
    scheme['e']           = base
    scheme['sprime']      = base
    scheme['eprime']      = base + u_ct
    scheme['eprimeprime'] = base + u2
    scheme['n']           = 256 * m
    scheme['n2']          = 256
    return scheme