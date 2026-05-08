from math import log
from new_distribution_failure import build_exact_distribution, build_limiting_distribution, p2_cyclotomic_error_probability
from MLWE_security import MLWE_summarize_attacks, MLWEParameterSet
from proba_util import build_mod_switching_error_law

class KyberParameterSet:
    def __init__(self, n, m, ks, ke,  q, rqk, rqc, rq2, ke_ct=None):
        if ke_ct is None:
            ke_ct = ke
        self.n = n
        self.m = m
        self.ks = ks     # binary distribution for the secret key
        self.ke = ke    # binary distribution for the ciphertext errors
        self.ke_ct = ke_ct    # binary distribution for the ciphertext errors
        self.q = q
        self.rqk = rqk  # 2^(bits in the public key)
        self.rqc = rqc  # 2^(bits in the first ciphertext)
        self.rq2 = rq2  # 2^(bits in the second ciphertext)


def Kyber_to_MLWE(kps):
    if kps.ks != kps.ke:
        raise "The security script does not handle different error parameter in secrets and errors (ks != ke) "

    # Check whether ciphertext error variance after rounding is larger than secret key error variance
    Rc = build_mod_switching_error_law(kps.q, kps.rqc)
    var_rounding = sum([i*i*Rc[i] for i in Rc.keys()])

    if kps.ke_ct/2. + var_rounding < kps.ke/2.:
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

if __name__ == "__main__":
#     params = [
#         # (label,         n,   m, ks, ke,   q,     rqk,   rqc,   rq2)
#         ("256*24, f(8)",  256,  24,  8,  8, 3329, 2**12, 2**12, 2**12),
#     ]
    params = [
    (f"256*{m}", 256, m, n, n, 3329, 2**12, 2**12, 2**12)
    for m in range(8, 30)
    for n in range(4, 20)
]

#     params = [
#     ("256*24, f(8),  rq2=2^12", 256, 24,  8,  8, 3329, 2**12, 2**12, 2**12),
#     ("256*24, f(9),  rq2=2^12", 256, 24,  9,  9, 3329, 2**12, 2**12, 2**12),
#     ("256*24, f(10), rq2=2^12", 256, 24, 10, 10, 3329, 2**12, 2**12, 2**12),
#     ("256*24, f(11), rq2=2^12", 256, 24, 11, 11, 3329, 2**12, 2**12, 2**12),
#     ("256*24, f(12), rq2=2^12", 256, 24, 12, 12, 3329, 2**12, 2**12, 2**12),
#     ("256*24, f(15), rq2=2^12", 256, 24, 15, 15, 3329, 2**12, 2**12, 2**12),
#     ("256*24, f(20), rq2=2^12", 256, 24, 20, 20, 3329, 2**12, 2**12, 2**12),
#     ("256*24, f(24), rq2=2^12", 256, 24, 24, 24, 3329, 2**12, 2**12, 2**12),
#     ("256*24, f(30), rq2=2^12", 256, 24, 30, 30, 3329, 2**12, 2**12, 2**12),
# ]


#     params = [
#     # m=25, vary rq2 compression
#     ("256*25, f(8), rq2=2^12", 256, 25, 8, 8, 3329, 2**12, 2**12, 2**12),
#     ("256*25, f(8), rq2=2^11", 256, 25, 8, 8, 3329, 2**12, 2**12, 2**11),
#     ("256*25, f(8), rq2=2^10", 256, 25, 8, 8, 3329, 2**12, 2**12, 2**10),
#     ("256*25, f(8), rq2=2^9",  256, 25, 8, 8, 3329, 2**12, 2**12, 2**9),
#     ("256*25, f(8), rq2=2^8",  256, 25, 8, 8, 3329, 2**12, 2**12, 2**8),
#     ("256*25, f(8), rq2=2^7",  256, 25, 8, 8, 3329, 2**12, 2**12, 2**7),
#     ("256*25, f(8), rq2=2^6",  256, 25, 8, 8, 3329, 2**12, 2**12, 2**6),
#     ("256*25, f(8), rq2=2^5",  256, 25, 8, 8, 3329, 2**12, 2**12, 2**5),
#     ("256*25, f(8), rq2=2^4",  256, 25, 8, 8, 3329, 2**12, 2**12, 2**4),
# ]

# pk size is fixed at 9632 regardless of compression, so m = 25 is not acceptable within the budget
#     params = [
#     ("256*24, f(8), rq2=2^6", 256, 24, 8, 8, 3329, 2**12, 2**12, 2**6),
#     ("256*24, f(8), rq2=2^5", 256, 24, 8, 8, 3329, 2**12, 2**12, 2**5),
#     ("256*24, f(8), rq2=2^4", 256, 24, 8, 8, 3329, 2**12, 2**12, 2**4),
#     ("256*25, f(8), rq2=2^6", 256, 25, 8, 8, 3329, 2**12, 2**12, 2**6),
# ]

# 9616, 9752

# sizes at m = 25 will be always be higher regardless of which f(n) you use

    for label, n, m, ks, ke, q, rqk, rqc, rq2 in params:
        ps = KyberParameterSet(n, m, ks, ke, q, rqk, rqc, rq2)
        print(f"{label}:")
        print("--------------------")
        # print("security:")
        # MLWE_summarize_attacks(Kyber_to_MLWE(ps))
        F, f = p2_cyclotomic_error_probability(ps)
        # pk, ct = communication_costs(ps)
        print("failure:  2^%.1f" % (log(f + 2.**(-300))/log(2)))
        # print("pk size:  %.0f bytes" % pk)
        # print("ct size:  %.0f bytes" % ct)
        print()