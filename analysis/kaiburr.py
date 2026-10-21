from math import log
from new_distribution_failure import build_exact_distribution, build_limiting_distribution, p2_cyclotomic_error_probability
from MLWE_security import MLWE_summarize_attacks, MLWEParameterSet, variance_f
from proba_util import build_mod_switching_error_law

class KyberParameterSet:
    def __init__(self, n, m, ks, ke,  q, rqk, rqc, rq2, ke_ct=None, cbd=None):
        if ke_ct is None:
            ke_ct = ke
        self.n = n
        self.m = m
        self.ks = ks     # n in f(n) for secret key
        self.ke = ke     # n in f(n) for ciphertext errors
        self.ke_ct = ke_ct  # n in f(n) for ciphertext errors
        self.q = q
        self.rqk = rqk  # 2^(bits in the public key)
        self.rqc = rqc  # 2^(bits in the first ciphertext)
        self.rq2 = rq2  # 2^(bits in the second ciphertext)
        self.cbd = cbd  # if set, use centered binomial noise CBD(cbd) instead of f(n)

def Kyber_to_MLWE(kps):
    if kps.ks != kps.ke:
        raise "The security script does not handle different error parameter in secrets and errors (ks != ke) "

    # Check whether ciphertext error variance after rounding is larger than secret key error variance
    Rc = build_mod_switching_error_law(kps.q, kps.rqc)
    var_rounding = sum([i*i*Rc[i] for i in Rc.keys()])

    if variance_f(kps.ke_ct) + var_rounding < variance_f(kps.ke):
        raise "The security of the ciphertext MLWE may not be stronger than the one of the public key MLWE"    

    return MLWEParameterSet(kps.n, kps.m, kps.m + 1, kps.ks, kps.q)


def communication_costs(ps):
    """ Compute the communication cost of a parameter set
    :param ps: Parameter set (ParameterSet)
    :returns: (cost_Alice, cost_Bob) (in Bytes)
    """
    A_space = 256 + ps.n * ps.m * log(ps.rqk)/log(2)
    B_space = ps.n * ps.m * log(ps.rqc)/log(2) + ps.n * log(ps.rq2)/log(2)
    return (int(round(A_space))/8., int(round(B_space))/8.)

def get_distribution(n):
    if n >= 999:
        return build_limiting_distribution()
    else:
        return build_exact_distribution(n)


def summarize(ps):
    print ("params: ", ps.__dict__)
    print ("com costs: ", communication_costs(ps))
    F, f = p2_cyclotomic_error_probability(ps)
    print ("failure: %.1f = 2^%.1f"%(f, log(f + 2.**(-300))/log(2)))


def failure_exp(ps):
    F, f = p2_cyclotomic_error_probability(ps)
    return log(f + 2.**(-300))/log(2)


if __name__ == "__main__":
    import io, contextlib

    # n = 256, q = 3329, no ciphertext compression (rqk = rqc = rq2 = 2^12)

    # warmup table
    print("Warmup: decryption failure vs module rank k")
    print("k  | failure  | pk   | ct")
    for k in range(3, 9):
        ps = KyberParameterSet(256, k, 2, 2, 3329, 2**12, 2**12, 2**12, cbd=2)
        pk, ct = communication_costs(ps)
        print("%d  | 2^%.1f | %.0f | %.0f" % (k, failure_exp(ps), pk, ct))
    print()

    # parameter selection table
    # bound and FrodoKEM-640's budget (pk <= 9616, ct <= 9720 bytes)
    print("Parameter selection")
    print("scheme       | k  | noise | failure  | class. | quant. | pk   | ct")
    for t, k in [(2, 1), (3, 3), (4, 7), (5, 13), (6, 18), (7, 23), (8, 24)]:
        ps = KyberParameterSet(256, k, t, t, 3329, 2**12, 2**12, 2**12)
        with contextlib.redirect_stdout(io.StringIO()):
            b_pq, c_pc, c_pq, c_pp = MLWE_summarize_attacks(Kyber_to_MLWE(ps))
        pk, ct = communication_costs(ps)
        print("Kaiburr-%-4d | %-2d | f(%d)  | 2^%.1f | %-6d | %-6d | %.0f | %.0f"
              % (256*k, k, t, failure_exp(ps), c_pc, c_pq, pk, ct))
    print()

    # ceiling table
    print("Ceiling")
    print("k  | failure  | pk    | ct")
    for k in [24, 26, 28, 29, 30]:
        ps = KyberParameterSet(256, k, 999, 999, 3329, 2**12, 2**12, 2**12)
        pk, ct = communication_costs(ps)
        print("%d | 2^%.1f | %.0f | %.0f" % (k, failure_exp(ps), pk, ct))
