## testing two of vadim's suggested parameters
# (256*6,5,12,4)->(225,2336,2432)
# (256*7,5,12,6)->(196,2720,2656)

from math import log, log2, ceil
from kaiburr import KyberParameterSet, Kyber_to_MLWE, communication_costs
from MLWE_security import MLWE_summarize_attacks
from new_distribution_failure import p2_cyclotomic_error_probability
from utils import n_star_formula


# params = [
#     ("256*6", 256, 6, 5, 5, 3329, 2**12, 2**12, 2**4),
#     ("256*7", 256, 7, 5, 5, 3329, 2**12, 2**12, 2**6)
# ]

# for label, n, m, ks, ke, q, rqk, rqc, rq2 in params:
#         ps = KyberParameterSet(n, m, ks, ke, q, rqk, rqc, rq2)
#         print(f"{label}:")
#         print("--------------------")
#         print("security:")
#         MLWE_summarize_attacks(Kyber_to_MLWE(ps))
#         F, f = p2_cyclotomic_error_probability(ps)
#         pk, ct = communication_costs(ps)
#         per_ciphertext = log(f + 2.**(-300))/log(2)
#         per_coefficient = per_ciphertext - log2(ps.n)  # subtract log2(256) = 8
#         print("failure (per coeff):  2^%.1f" % per_coefficient)
#         print("pk size:  %.0f bytes" % pk)
#         print("ct size:  %.0f bytes" % ct)
#         print()

# frodo budgets
frodo_targets = [
    ("frodo640",  9616,  9720),
    ("frodo976",  15632, 15744),
    ("frodo1344", 21520, 21632),
]

qs = [3329, 7681]

print("\n\nSYSTEMATIC PARAMETER SEARCH")
print("=" * 90)
print(f"{'target':<12} {'q':<6} {'m':<5} {'n':<5} {'rq2':<8} {'pk':>8} {'ct':>8} {'fail/coeff':>12} {'MLWE_sec':>10}")
print("-" * 90)

for label, pk_budget, ct_budget in frodo_targets:
    for q in qs:
        rqk = 2**ceil(log2(q + 1))
        
        # find max m under pk budget
        m_best = None
        for m in range(1, 200):
            ps = KyberParameterSet(256, m, 16, 16, q, rqk, rqk, rqk)
            pk, ct = communication_costs(ps)
            if pk < pk_budget:
                m_best = m
            else:
                break
        
        if m_best is None:
            continue

        # find n = n_star(m)
        n = n_star_formula(m_best)

        # find max rq2 that fits ct under budget
        rq2_best = None
        for rq2_exp in range(ceil(log2(q + 1)), 6, -1):
            ps = KyberParameterSet(256, m_best, n, n, q, rqk, rqk, 2**rq2_exp)
            pk, ct = communication_costs(ps)
            if ct < ct_budget:
                rq2_best = rq2_exp
                break

        if rq2_best is None:
            continue

        ps = KyberParameterSet(256, m_best, n, n, q, rqk, rqk, 2**rq2_best)
        pk, ct = communication_costs(ps)
        F, f = p2_cyclotomic_error_probability(ps)
        decryption_failure = log(f + 2.**(-300))/log(2)
        mlwe = Kyber_to_MLWE(ps)

        print(f"{label:<12} {q:<6} {m_best:<5} {n:<5} 2^{rq2_best:<6} {pk:>8.0f} {ct:>8.0f} {decryption_failure:>12.1f}", end="")
        print()