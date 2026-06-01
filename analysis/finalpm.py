import csv
from math import log, log2, ceil
from multiprocessing import Pool
from kaiburr import KyberParameterSet, communication_costs, MLWE_summarize_attacks, Kyber_to_MLWE
from new_distribution_failure import p2_cyclotomic_error_probability
from utils import find_min_n

## fn is for the n in fn

def run_param(args):
    label, ring_dim, m, fn, ke, q, rqk, rqc, rq2 = args
    ps = KyberParameterSet(ring_dim, m, fn, ke, q, rqk, rqc, rq2)
    F, f = p2_cyclotomic_error_probability(ps)
    failure = log(f + 2.**(-300)) / log(2)
    pk, ct = communication_costs(ps)
    b_pq, c_pc, c_pq, c_pp = MLWE_summarize_attacks(Kyber_to_MLWE(ps))
    return (label, round(failure, 1), round(pk), round(ct), c_pc, c_pq, c_pp)

if __name__ == "__main__":
    params = []
    for m in range(5, 31):
        q = 3329
        rq = 2**ceil(log2(q + 1))
        fn, _ = find_min_n(m, q)
        params.append((f"m={m},q={q},fn={fn}", 256, m, fn, fn, q, rq, rq, rq))
    for m in range(5, 159):
        q = 7681
        rq = 2**ceil(log2(q + 1))
        fn, _ = find_min_n(m, q)
        params.append((f"m={m},q={q},fn={fn}", 256, m, fn, fn, q, rq, rq, rq))

    with Pool(processes=len(params)) as pool:
        results = pool.map(run_param, params)

    with open("minn.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["label", "failure (2^x)", "pk (bytes)", "ct (bytes)", "classical", "quantum", "plausible"])
        for row in results:
            writer.writerow(row)

    print("Done.")