# scheme        sk        pk        c      ss
# frodokem640  19888     9616      9720    16
# frodokem976  31296     15632     15744   24
# frodokem1344 43088     21520     21632   32

from kaiburr import KyberParameterSet, communication_costs

# pk and ct sizes for n=256, q=3329, no compression, fixing n = 16 because it has no effect on size

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


# find max m for which the pk and c size are just below frodo1344 without compression
# with q = 7681

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

# largest m (q=7681) with pk < 21520 and ct < 21632:
#   m=50, pk=20832, ct=21216

# find max m for which the pk and c size are just below frodo976
# with q = 3329 and 7681

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

# largest m (q=3329) with pk < 15632 and ct < 15744:
#   m=39, pk=15008, ct=15360 ::: failure probability explodes here, not valid

# largest m (q=7681) with pk < 15632 and ct < 15744:
#   m=36, pk=15008, ct=15392