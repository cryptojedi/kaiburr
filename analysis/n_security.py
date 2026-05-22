# evaluating how security changes with increase in n for a small parameter

from kaiburr import KyberParameterSet, MLWE_summarize_attacks, Kyber_to_MLWE
from new_distribution_failure import p2_cyclotomic_error_probability
from math import log
from multiprocessing import Pool
import csv

def run_param(args):
    label, n, m, ks, ke, q, rqk, rqc, rq2 = args
    ps = KyberParameterSet(n, m, ks, ke, q, rqk, rqc, rq2)
    F, f = p2_cyclotomic_error_probability(ps)
    failure = log(f + 2.**(-1000)) / log(2)
    b_pq, c_pc, c_pq, c_pp = MLWE_summarize_attacks(Kyber_to_MLWE(ps))
    return (ks, failure, c_pc, c_pq, c_pp)

if __name__ == "__main__":
    params = [
        (f"256*3, f({n})", 256, 3, n, n, 3329, 2**12, 2**12, 2**12)
        for n in range(4, 26)
    ]
    with Pool(processes=len(params)) as pool:
        results = pool.map(run_param, params)

    results.sort(key=lambda x: x[0])

    with open("n_security.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "failure (2^x)", "classical", "quantum", "plausible"])
        for row in results:
            writer.writerow([row[0], f"{row[1]:.1f}", row[2], row[3], row[4]])

    print(f"{'f(n)':<6} {'failure':>12} {'classical':>12} {'quantum':>12} {'plausible':>12}")
    print("-" * 56)
    for row in results:
        print(f"{row[0]:<6} {row[1]:>12.1f} {row[2]:>12} {row[3]:>12} {row[4]:>12}")