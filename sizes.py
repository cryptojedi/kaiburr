# scheme        sk        pk        c      ss
# frodokem640  19888     9616      9720    16
# frodokem976  31296     15632     15744   24
# frodokem1344 43088     21520     21632   32

from math import log, ceil, log2
from kaiburr import KyberParameterSet, communication_costs
from new_distribution_failure import p2_cyclotomic_error_probability

# # pk and ct sizes for n=256, q=3329, no compression, fixing n = 16 because it has no effect on size

print(f"{'scheme':<22} {'pk (bytes)':>12} {'ct (bytes)':>12}")
print("-" * 48)
for m in range(20, 31):
    ps = KyberParameterSet(256, m, 16, 16, 3329, 2**12, 2**12, 2**12)
    pk, ct = communication_costs(ps)
    print(f"{'256x'+str(m)+', q=3329':<22} {pk:>12.0f} {ct:>12.0f}")


print(f"{'scheme':<22} {'pk (bytes)':>12} {'ct (bytes)':>12}")
print("-" * 48)
for m in range(150, 160):
    ps = KyberParameterSet(256, m, 16, 16, 7681, 2**13, 2**13, 2**13)
    pk, ct = communication_costs(ps)
    print(f"{'256x'+str(m)+', q=7681':<22} {pk:>12.0f} {ct:>12.0f}")

# # 256x20, q=7681                 8352         8736
# # 256x21, q=7681                 8768         9152
# # 256x22, q=7681                 9184         9568
# # 256x23, q=7681                 9600         9984
# # 256x24, q=7681                10016        10400
# # 256x25, q=7681                10432        10816


# # find max m for which the pk and c size are just below frodo1344 without compression
# # with q = 7681

frodo1344_pk = 21520
frodo1344_ct = 21632

m_best = None
for m in range(1, 158):
    ps = KyberParameterSet(256, m, 16, 16, 7681, 2**13, 2**13, 2**13)
    pk, ct = communication_costs(ps)
    if pk < frodo1344_pk and ct < frodo1344_ct:
        m_best, pk_best, ct_best = m, pk, ct
    else:
        break

print(f"\nlargest m (q=7681) with pk < {frodo1344_pk} and ct < {frodo1344_ct}:")
print(f"  m={m_best}, pk={pk_best:.0f}, ct={ct_best:.0f}")

# # largest m (q=7681) with pk < 21520 and ct < 21632:
# #   m=50, pk=20832, ct=21216

# # find max m for which the pk and c size are just below frodo976
# # with q = 3329 and 7681

frodo976_pk = 15632
frodo976_ct = 15744

m_best = None
for m in range(1, 1000):
    ps = KyberParameterSet(256, m, 16, 16, 3329, 2**12, 2**12, 2**12)
    pk, ct = communication_costs(ps)
    if pk < frodo976_pk and ct < frodo976_ct:
        m_best, pk_best, ct_best = m, pk, ct
    else:
        break

print(f"\nlargest m (q=3329) with pk < {frodo976_pk} and ct < {frodo976_ct}:")
print(f"  m={m_best}, pk={pk_best:.0f}, ct={ct_best:.0f}")

m_best = None
for m in range(1, 1000):
    ps = KyberParameterSet(256, m, 16, 16, 7681, 2**13, 2**13, 2**13)
    pk, ct = communication_costs(ps)
    if pk < frodo976_pk and ct < frodo976_ct:
        m_best, pk_best, ct_best = m, pk, ct
    else:
        break

print(f"\nlargest m (q=7681) with pk < {frodo976_pk} and ct < {frodo976_ct}:")
print(f"  m={m_best}, pk={pk_best:.0f}, ct={ct_best:.0f}")

# # largest m (q=3329) with pk < 15632 and ct < 15744:
# #   m=39, pk=15008, ct=15360 ::: failure probability explodes here, not valid

# # largest m (q=7681) with pk < 15632 and ct < 15744:
# #   m=36, pk=15008, ct=15392


q = 7681
rqk = 2**ceil(log2(q + 1))

frodo_targets = [
    ("frodo640",  9616,  9720,  23),
    ("frodo976",  15632, 15744, 37),
    ("frodo1344", 21520, 21632, 51),
]

for label, pk_budget, ct_budget, m in frodo_targets:
    print(f"m = {m}, q = {q}, target = {label} (pk < {pk_budget}, ct < {ct_budget})")
    print()
    print(f"{'n':<6} {'rq2':<8} {'pk':>9} {'ct':>9} {'fits?':>7} {'failure':>14} {'delta':>10}")
    print("-" * 70)

    for n in [8, 10, 12, 15, 20]:
        prev_fail = None
        for rq2_exp in range(ceil(log2(q + 1)), 6, -1):
            ps = KyberParameterSet(256, m, n, n, q, rqk, rqk, 2**rq2_exp)
            pk, ct = communication_costs(ps)
            F, f = p2_cyclotomic_error_probability(ps)
            fail = log(f + 2.**(-1000)) / log(2)
            fits = "YES" if pk < pk_budget and ct < ct_budget else "no"
            delta = f"{abs(fail - prev_fail):.2f}" if prev_fail is not None else "—"
            print(f"{n:<6} 2^{rq2_exp:<6} {pk:>9.0f} {ct:>9.0f} {fits:>7} {'2^'+f'{fail:.1f}':>14} {delta:>10}")
            prev_fail = fail
        print()

    print()

# m = 37, q = 7681, target = frodo976 (pk < 15632, ct < 15744)

# n      rq2             pk        ct   fits?        failure      delta
# ----------------------------------------------------------------------
# 8      2^13         15424     15808      no       2^-491.9          —
# 8      2^12         15424     15776      no       2^-491.8       0.04
# 8      2^11         15424     15744      no       2^-491.7       0.08
# 8      2^10         15424     15712     YES       2^-491.4       0.30
# 8      2^9          15424     15680     YES       2^-490.4       1.00
# 8      2^8          15424     15648     YES       2^-487.6       2.87
# 8      2^7          15424     15616     YES       2^-480.9       6.63

# 10     2^13         15424     15808      no       2^-540.0          —
# 10     2^12         15424     15776      no       2^-540.0       0.05
# 10     2^11         15424     15744      no       2^-539.9       0.10
# 10     2^10         15424     15712     YES       2^-539.5       0.37
# 10     2^9          15424     15680     YES       2^-538.3       1.20
# 10     2^8          15424     15648     YES       2^-535.0       3.32
# 10     2^7          15424     15616     YES       2^-527.5       7.49

# 12     2^13         15424     15808      no       2^-553.5          —
# 12     2^12         15424     15776      no       2^-553.4       0.06
# 12     2^11         15424     15744      no       2^-553.3       0.11
# 12     2^10         15424     15712     YES       2^-552.9       0.39
# 12     2^9          15424     15680     YES       2^-551.6       1.28
# 12     2^8          15424     15648     YES       2^-548.1       3.49
# 12     2^7          15424     15616     YES       2^-540.3       7.79

# 15     2^13         15424     15808      no       2^-557.5          —
# 15     2^12         15424     15776      no       2^-557.5       0.06
# 15     2^11         15424     15744      no       2^-557.3       0.11
# 15     2^10         15424     15712     YES       2^-556.9       0.40
# 15     2^9          15424     15680     YES       2^-555.6       1.31
# 15     2^8          15424     15648     YES       2^-552.1       3.54
# 15     2^7          15424     15616     YES       2^-544.2       7.88

# 20     2^13         15424     15808      no       2^-558.1          —
# 20     2^12         15424     15776      no       2^-558.1       0.06
# 20     2^11         15424     15744      no       2^-557.9       0.11
# 20     2^10         15424     15712     YES       2^-557.5       0.41
# 20     2^9          15424     15680     YES       2^-556.2       1.31
# 20     2^8          15424     15648     YES       2^-552.7       3.56
# 20     2^7          15424     15616     YES       2^-544.8       7.91


# m = 51, q = 7681, target = frodo1344 (pk < 21520, ct < 21632)

# n      rq2             pk        ct   fits?        failure      delta
# ----------------------------------------------------------------------
# 8      2^13         21248     21632      no       2^-356.7          —
# 8      2^12         21248     21600     YES       2^-356.7       0.02
# 8      2^11         21248     21568     YES       2^-356.7       0.04
# 8      2^10         21248     21536     YES       2^-356.5       0.16
# 8      2^9          21248     21504     YES       2^-355.9       0.59
# 8      2^8          21248     21472     YES       2^-354.1       1.84
# 8      2^7          21248     21440     YES       2^-349.5       4.56

# 10     2^13         21248     21632      no       2^-391.1          —
# 10     2^12         21248     21600     YES       2^-391.1       0.03
# 10     2^11         21248     21568     YES       2^-391.0       0.05
# 10     2^10         21248     21536     YES       2^-390.9       0.19
# 10     2^9          21248     21504     YES       2^-390.2       0.69
# 10     2^8          21248     21472     YES       2^-388.1       2.10
# 10     2^7          21248     21440     YES       2^-383.0       5.10

# 12     2^13         21248     21632      no       2^-400.5          —
# 12     2^12         21248     21600     YES       2^-400.5       0.03
# 12     2^11         21248     21568     YES       2^-400.4       0.05
# 12     2^10         21248     21536     YES       2^-400.2       0.20
# 12     2^9          21248     21504     YES       2^-399.5       0.72
# 12     2^8          21248     21472     YES       2^-397.3       2.17
# 12     2^7          21248     21440     YES       2^-392.1       5.24

# 15     2^13         21248     21632      no       2^-403.3          —
# 15     2^12         21248     21600     YES       2^-403.3       0.03
# 15     2^11         21248     21568     YES       2^-403.2       0.05
# 15     2^10         21248     21536     YES       2^-403.0       0.20
# 15     2^9          21248     21504     YES       2^-402.3       0.72
# 15     2^8          21248     21472     YES       2^-400.1       2.19
# 15     2^7          21248     21440     YES       2^-394.8       5.29

# 20     2^13         21248     21632      no       2^-403.7          —
# 20     2^12         21248     21600     YES       2^-403.7       0.03
# 20     2^11         21248     21568     YES       2^-403.6       0.05
# 20     2^10         21248     21536     YES       2^-403.4       0.21
# 20     2^9          21248     21504     YES       2^-402.7       0.73
# 20     2^8          21248     21472     YES       2^-400.5       2.20
# 20     2^7          21248     21440     YES       2^-395.2       5.29