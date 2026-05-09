from math import log2, ceil
from utils import get_failure_exp, expected_pm2, n_star_formula
import matplotlib.pyplot as plt

def pm2_table(m):
    total_polys = (4*m + 1)
    
    print(f"m = {m}, total polynomials = {total_polys}")
    print()
    print(f"{'n':<6} {'Pr[±2]':<12} {'E[#±2] per poly':<20} {'E[#±2] total':<20} {'Pr[no ±2 in poly]':<22} {'failure prob (2^x)'}")
    print("-" * 110)
    
    for n in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
        pr2 = 0.5**n
        expected_total = expected_pm2(n, m)
        expected_per = expected_total / total_polys
        pr_no_pm2 = (1 - 2*pr2)**256
        fail = get_failure_exp(m, n)
        print(f"{n:<6} {pr2:<12.8f} {expected_per:<20.4f} {expected_total:<20.4f} {pr_no_pm2:<22.6f} {fail:.1f}")


def threshold_table(m):
    print(f"m = {m}, total polynomials = {4*m+1}")
    print()
    print(f"{'n':<6} {'E[#±2] total':<18} {'above/below 1':<16} {'fail prob (2^x)':<20} {'delta fail':<12} {'ratio'}")
    print("-" * 80)
    
    prev_fail = None
    for n in range(4, 21):
        fail = get_failure_exp(m, n)
        e = expected_pm2(n, m)
        above = "above 1" if e >= 1 else "below 1"
        
        if prev_fail is not None:
            delta = abs(fail - prev_fail)
            ratio = delta / e if e > 0 else 0
            print(f"{n:<6} {e:<18.4f} {above:<16} {fail:<20.1f} {delta:<12.4f} {ratio:.6f}")
        else:
            print(f"{n:<6} {e:<18.4f} {above:<16} {fail:<20.1f} {'—':<12} {'—'}")
        
        prev_fail = fail

def find_n_failure(m, n_range=range(4, 25), threshold=-128):
    prev_fail = None
    for n in n_range:
        fail = get_failure_exp(m, n)
        if fail <= threshold:
            return n, fail
        prev_fail = fail
    return None, None

def n_failure_table():
    print(f"{'m':<6} {'n_failure':<12} {'failure prob (2^x)'}")
    print("-" * 35)
    for m in range(8, 30):
        n_fail, fp = find_n_failure(m)
        if n_fail:
            print(f"{m:<6} {n_fail:<12} {fp:.1f}")
        else:
            print(f"{m:<6} {'none':<12} below threshold always")

def threshold_formula_table():
    print(f"{'m':<6} {'(4m+1)*512':<14} {'log2':<12} {'n*(m)'}")
    print("-" * 40)
    for m in range(8, 30):
        val = (4*m + 1) * 512
        log_val = log2(val)
        print(f"{m:<6} {val:<14} {log_val:<12.4f} {n_star_formula(m)}")

# def plot_failure_prob(m_values=[15, 24, 29]):  # check for more dimensions later
#     n_range = list(range(4, 25))
#     plt.figure(figsize=(9, 5))

#     for m in m_values:
#         fail_probs = [get_failure_exp(m, n) for n in n_range]
#         plt.plot(n_range, fail_probs, marker='o', label=f'm = {m}')

#     # security threshold
#     plt.axhline(y=-128, color='black', linestyle='--', linewidth=1.2, label='threshold = 2⁻¹²⁸')
#     plt.xlabel('n')
#     plt.ylabel('Failure probability exponent (x in 2^x)')
#     plt.title('Failure probability vs n')
#     plt.legend()
#     plt.grid(True, alpha=0.3)
#     plt.tight_layout()
#     plt.savefig('failure_prob.png', dpi=150)
#     plt.show()

if __name__ == "__main__":
    
    # pm2 table for specific dimensions
    for m in [7, 10, 13, 16, 19, 21, 24, 27, 29, 31]:
        pm2_table(m)
        print()

    # threshold table for specific dimensions  
    for m in [7, 10, 13, 16, 19, 21, 24, 27, 29, 31]:
        threshold_table(m)
        print()

    # n_failure for all dimensions
    print("n_failure(m) table:")
    n_failure_table()
    print()

    # threshold formula verification
    print("Threshold formula n*(m):")
    threshold_formula_table()

    # plot of failure probability vs n
    # plot_failure_prob(m_values=[15, 24, 29])


# # ## why n =n 16?

# # for m in range(8, 30):
# #     val = (4*m + 1) * 512
# #     log_val = log2(val)
# #     threshold = int(log_val) + 1  # ceiling
# #     print(f"m={m:<4} (4m+1)*512={val:<8} log2={log_val:.4f} threshold n={threshold}")