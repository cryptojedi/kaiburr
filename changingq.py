from math import log
from new_distribution_failure import build_exact_distribution, build_limiting_distribution, p2_cyclotomic_error_probability
from MLWE_security import MLWE_summarize_attacks, MLWEParameterSet
from proba_util import build_mod_switching_error_law

class KyberParameterSet:
    def __init__(self, n, m, ks, ke, q, rqk, rqc, rq2, ke_ct=None):
        if ke_ct is None:
            ke_ct = ke
        self.n = n
        self.m = m
        self.ks = ks
        self.ke = ke
        self.ke_ct = ke_ct
        self.q = q
        self.rqk = rqk
        self.rqc = rqc
        self.rq2 = rq2

def get_failure_exp(m, n, q):
    ps = KyberParameterSet(256, m, n, n, q, 2**12, 2**12, 2**12)
    F, f = p2_cyclotomic_error_probability(ps)
    return log(f + 2.**(-1000)) / log(2)

def communication_costs(ps):
    A_space = 256 + ps.n * ps.m * log(ps.rqk)/log(2)
    B_space = ps.n * ps.m * log(ps.rqc)/log(2) + ps.n * log(ps.rq2)/log(2)
    return (int(round(A_space))/8., int(round(B_space))/8.)

m = 10
q1, q2 = 3329, 7629

print(f"m = {m}, q = {q1} vs q = {q2}")
print()
print(f"{'n':<6} {'fail q=3329':>14} {'pk':>9} {'ct':>9}   {'fail q=769':>14} {'pk':>9} {'ct':>9}")
print("-" * 80)

# NOTE: original kyber security proofs only apply to a variant that does not compress the public key

for n in range(4, 26):
    f1 = get_failure_exp(m, n, q1)
    f2 = get_failure_exp(m, n, q2)
    ps1 = KyberParameterSet(256, m, n, n, q1, 2**12, 2**12, 2**12)
    ps2 = KyberParameterSet(256, m, n, n, q2, 2**13, 2**13, 2**13)
    pk1, ct1 = communication_costs(ps1)
    pk2, ct2 = communication_costs(ps2)
    print(f"{n:<6} {'2^'+f'{f1:.1f}':>14} {pk1:>8.0f} {ct1:>8.0f} {'2^'+f'{f2:.1f}':>14} {pk2:>8.0f} {ct2:>8.0f}")

## question worth considering: should we go for a lower value of q or keep going higher?
# how does it change the ciphertext and public key size?

# question worth considering: should we go for a lower value of q or keep going higher?
# how does it change the ciphertext and public key size? 

n = 16
q = 769
for m in range(25, 51):
    f = get_failure_exp(m, n, q)
    ps = KyberParameterSet(256, m, n, n, q, 2**10, 2**10, 2**10)
    pk, ct = communication_costs(ps)
    print(f"{m:<6} {'2^'+f'{f:.1f}':>14} {pk:>8.0f} {ct:>8.0f}")