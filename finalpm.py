import csv
from math import log, log2, ceil
from multiprocessing import Pool
from kaiburr import KyberParameterSet, communication_costs, MLWE_summarize_attacks, Kyber_to_MLWE
from new_distribution_failure import p2_cyclotomic_error_probability
from utils import n_star_formula

def get_row(args):
    m, q = args
    rq = 2**ceil(log2(q + 1))
    n = n_star_formula(m)
    ps = KyberParameterSet(256, m, n, n, q, rq, rq, rq)
    F, f = p2_cyclotomic_error_probability(ps)
    failure = log(f + 2.**(-300)) / log(2)
    pk, ct = communication_costs(ps)
    return (m, q, n, round(failure, 1), round(pk), round(ct))

def run_param(args):
    label, n, m, ks, ke, q, rqk, rqc, rq2 = args
    ps = KyberParameterSet(n, m, ks, ke, q, rqk, rqc, rq2)
    F, f = p2_cyclotomic_error_probability(ps)
    failure = log(f + 2.**(-300)) / log(2)
    pk, ct = communication_costs(ps)
    b_pq, c_pc, c_pq, c_pp = MLWE_summarize_attacks(Kyber_to_MLWE(ps))
    return (label, failure, pk, ct, c_pc, c_pq, c_pp)

if __name__ == "__main__":
    # params = [(m, 3329) for m in range(5, 31)] + [(m, 7681) for m in range(5, 159)]

    # with Pool() as pool:
    #     rows = pool.map(get_row, params)

    # rows.sort(key=lambda x: (x[1], x[0]))

    # with open("finalpm.csv", "w", newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["m", "q", "n*(m)", "failure (2^x)", "pk (bytes)", "ct (bytes)"])
    #     writer.writerows(rows)

    # print(f"{'m':<6} {'q':<6} {'n*(m)':<8} {'failure':>12} {'pk':>10} {'ct':>10}")
    # print("-" * 55)
    # for row in rows:
    #     print(f"{row[0]:<6} {row[1]:<6} {row[2]:<8} {row[3]:>12} {row[4]:>10} {row[5]:>10}")
    
    params = [
        (f"256*24, f({n_star_formula(24)}), q=3329", 256, 24, n_star_formula(24), n_star_formula(24), 3329, 2**12, 2**12, 2**12),
        (f"256*22, f({n_star_formula(22)}), q=7681", 256, 22, n_star_formula(22), n_star_formula(22), 7681, 2**13, 2**13, 2**13),
        (f"256*36, f({n_star_formula(36)}), q=7681", 256, 36, n_star_formula(36), n_star_formula(36), 7681, 2**13, 2**13, 2**13),
        (f"256*51, f({n_star_formula(51)}), q=7681", 256, 51, n_star_formula(51), n_star_formula(51), 7681, 2**13, 2**13, 2**13),
    ]
    with Pool(processes=len(params)) as pool:
        results = pool.map(run_param, params)

    with open("security_estimates.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["label", "failure (2^x)", "pk (bytes)", "ct (bytes)", "classical", "quantum", "plausible"])
        for row in results:
            writer.writerow(row)

    print("Done.")