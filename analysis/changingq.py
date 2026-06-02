from math import log, ceil, log2
from kaiburr import KyberParameterSet, communication_costs, MLWE_summarize_attacks, MLWEParameterSet, Kyber_to_MLWE
from utils import get_failure_exp

# m = 157
# q1, q2 = 3329, 7681
# rq1 = 2**ceil(log2(q1 + 1))  # 4096 for q=3329
# rq2 = 2**ceil(log2(q2 + 1))  # 8192 for q=7681

# print(f"m = {m}, q = {q1} vs q = {q2}")
# print()
# print(f"{'n':<6} {'fail q=3329':>14} {'pk':>9} {'ct':>9}   {'fail q=7681':>14} {'pk':>9} {'ct':>9}")
# print("-" * 80)

# # NOTE: original security proofs only apply when you don't compress the public key (?)

# for n in range(4, 26):
#     f1 = get_failure_exp(m, n, q1)
#     f2 = get_failure_exp(m, n, q2)
#     ps1 = KyberParameterSet(256, m, n, n, q1, rq1, rq1, rq1)
#     ps2 = KyberParameterSet(256, m, n, n, q2, rq2, rq2, rq2)
#     pk1, ct1 = communication_costs(ps1)
#     pk2, ct2 = communication_costs(ps2)
#     print(f"{n:<6} {'2^'+f'{f1:.1f}':>14} {pk1:>8.0f} {ct1:>8.0f} {'2^'+f'{f2:.1f}':>14} {pk2:>8.0f} {ct2:>8.0f}")

# # assuming that by n = 20, the probability has most likely already plateaued

# n = 20
# q = 7681
# rq = 2**ceil(log2(q + 1))
# for m in range(151, 201):
#     f = get_failure_exp(m, n, q)
#     ps = KyberParameterSet(256, m, n, n, q, rq, rq, rq)
#     pk, ct = communication_costs(ps)
#     print(f"{m:<6} {'2^'+f'{f:.1f}':>14} {pk:>8.0f} {ct:>8.0f}")

# # the highest we can go with q = 7681 is m = 157; at m = 158, 
# # we get an approx max failure of 2^127.6, just below the threshold

# # question worth considering: should we go for a lower value of q or keep going higher?
# # how does it change the ciphertext and public key size? 

# n = 20
# q = 769
# rq = 2**ceil(log2(q + 1))
# for m in range(25, 51):
#     f = get_failure_exp(m, n, q)
#     ps = KyberParameterSet(256, m, n, n, q, rq, rq, rq)
#     pk, ct = communication_costs(ps)
#     print(f"{m:<6} {'2^'+f'{f:.1f}':>14} {pk:>8.0f} {ct:>8.0f}")

m = 3
n = 4
for q, rq2 in [(3329, 2**12), (7681, 2**13)]:
    ps = KyberParameterSet(256, m, n, n, q, rq2, rq2, rq2)
    _, c_cl, c_qu, _ = MLWE_summarize_attacks(Kyber_to_MLWE(ps))
    print(f"q={q}: classical={c_cl}, quantum={c_qu}")