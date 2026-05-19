from utils import n_star_formula
from math import ceil, log2
from dist import Dist
from analysis.new_distribution_failure import build_exact_distribution
from analysis.proba_util import build_mod_switching_error_law

def make_kaiburr_scheme(m, n, q, rq2=None):
    if rq2 is None:
        rq2 = 2**ceil(log2(q + 1))
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

target_params = [
    (24, n_star_formula(24), 3329),
    (22, n_star_formula(22), 7681),
    (36, n_star_formula(36), 7681),
    (51, n_star_formula(51), 7681),
]