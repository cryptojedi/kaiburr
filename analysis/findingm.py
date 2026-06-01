from math import log
from new_distribution_failure import p2_cyclotomic_error_probability
from MLWE_security import MLWE_summarize_attacks, MLWEParameterSet
from kaiburr import KyberParameterSet, Kyber_to_MLWE, communication_costs
from multiprocessing import Pool

def get_failure_exp(m, n, q):
    ps = KyberParameterSet(256, m, n, n, q, 2**12, 2**12, 2**12)
    F, f = p2_cyclotomic_error_probability(ps)
    return log(f + 2.**(-1000)) / log(2)

def find_min_m(n, q, threshold=-128):
    """minimum m where failure first crosses below threshold"""
    for m in range(4, 200):
        fail = get_failure_exp(m, n, q)
        if fail <= threshold:
            return m, fail
    return None, None

def find_max_m(n, q, threshold=-128):
    """maximum m where failure is still below threshold"""
    last_good = None
    for m in range(4, 200):
        fail = get_failure_exp(m, n, q)
        if fail <= threshold:
            last_good = (m, fail)
        else:
            return last_good
    return last_good

def run_param(args):
    n, m, q = args
    ps = KyberParameterSet(256, m, n, n, q, 2**12, 2**12, 2**12)
    F, f = p2_cyclotomic_error_probability(ps)
    failure = log(f + 2.**(-1000)) / log(2)
    mlwe = Kyber_to_MLWE(ps)
    b_pq, c_pc, c_pq, c_pp = MLWE_summarize_attacks(mlwe)
    pk, ct = communication_costs(ps)
    return (n, m, q, failure, c_pc, c_pq, c_pp, pk, ct)

if __name__ == "__main__":
    param_sets = [
        (4, 3329),
        (6, 3329),
        (8, 3329),
        (4, 7681),
        (6, 7681),
        (8, 7681)
    ]

    jobs = []
    for n, q in param_sets:
        min_m, _ = find_min_m(n, q)
        max_m, _ = find_max_m(n, q)
        if min_m and max_m:
            print(f"n={n}, q={q}: min_m={min_m}, max_m={max_m}")
            for m in range(min_m, max_m + 1):
                jobs.append((n, m, q))

    with Pool() as pool:
        results = pool.map(run_param, jobs)

    results.sort(key=lambda x: (x[2], x[0], x[1]))  # sort by q, n, m

    print(f"\n{'q':<8} {'n':<6} {'m':<6} {'failure':>12} {'classical':>12} {'quantum':>12} {'plausible':>12} {'pk (B)':>10} {'ct (B)':>10}")
    print("-" * 90)
    for r in results:
        n, m, q, fail, c_pc, c_pq, c_pp, pk, ct = r
        print(f"{q:<8} {n:<6} {m:<6} {fail:>12.1f} {c_pc:>12} {c_pq:>12} {c_pp:>12} {pk:>10.0f} {ct:>10.0f}")