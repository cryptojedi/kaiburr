import csv
from math import log, log2, ceil
from multiprocessing import Pool
from kaiburr import KyberParameterSet, communication_costs
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

if __name__ == "__main__":
    params = [(m, 3329) for m in range(5, 31)] + [(m, 7681) for m in range(5, 159)]

    with Pool() as pool:
        rows = pool.map(get_row, params)

    rows.sort(key=lambda x: (x[1], x[0]))

    with open("finalpm.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["m", "q", "n*(m)", "failure (2^x)", "pk (bytes)", "ct (bytes)"])
        writer.writerows(rows)

    print(f"{'m':<6} {'q':<6} {'n*(m)':<8} {'failure':>12} {'pk':>10} {'ct':>10}")
    print("-" * 55)
    for row in rows:
        print(f"{row[0]:<6} {row[1]:<6} {row[2]:<8} {row[3]:>12} {row[4]:>10} {row[5]:>10}")