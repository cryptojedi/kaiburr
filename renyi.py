# from math import sqrt, log, log2, ceil
# from utils import variance_f, f_n, Phi, chi, get_failure_exp, expected_pm2

# def renyi_per_sample(n_param, a=2.):
#     sig = sqrt(variance_f(n_param))
#     supp = [-2, -1, 0, 1, 2]
#     S = sum(f_n(i, n_param)**a / chi(i, sig)**(a-1) for i in supp)
#     return S**(1/(a-1))
# def renyi_static_table():
#     failure = {
#         8:  -139.9,
#         9:  -148.9,
#         10: -153.7,
#         11: -156.2,
#         12: -157.4,
#         15: -158.6,
#         20: -158.7,
#     }
    
#     print(f"{'n':<6} {'sigma':<10} {'Pr[±2]':<14} {'R_2 per sample':<18} {'failure (2^x)'}")
#     print("-" * 65)
#     for n in [4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20]:
#         sig = sqrt(variance_f(n))
#         pr2 = 0.5**n
#         r2 = renyi_per_sample(n, 2.)
#         fail = failure.get(n, "—")
#         print(f"{n:<6} {sig:<10.6f} {pr2:<14.8f} {r2:<18.8f} {fail}")

# def plateau_table(m):
#     print(f"\nm = {m} (theoretical ceiling at n*(m) = {ceil(log2((4*m+1)*512))})")
#     print(f"{'n':<6} {'failure (2^x)':<18} {'delta_fail':<14} {'R_2':<12} {'delta_R2':<12} {'E[#±2] total':<16} {'plateaued?'}")
#     print("-" * 90)
    
#     prev_fail = None
#     prev_r2 = None
    
#     for n in range(4, 25):
#         fail = get_failure_exp(m, n)
#         r2 = renyi_per_sample(n)
#         e_pm2 = expected_pm2(n, m)
        
#         if prev_fail is not None:
#             delta_fail = abs(fail - prev_fail)
#             delta_r2 = abs(r2 - prev_r2)
#             plateaued = "YES" if (delta_fail < 0.1 and delta_r2 < 0.0001) else "NO"
#             print(f"{n:<6} {fail:<18.1f} {delta_fail:<14.3f} {r2:<12.6f} {delta_r2:<12.6f} {e_pm2:<16.4f} {plateaued}")
#         else:
#             print(f"{n:<6} {fail:<18.1f} {'—':<14} {r2:<12.6f} {'—':<12} {e_pm2:<16.4f} {'—'}")
        
#         prev_fail = fail
#         prev_r2 = r2

# def plateau_summary():
#     print(f"{'m':<6} {'n_plateau':<12} {'E[#±2] at plateau':<22} {'fail at plateau':<20} {'R_2 at plateau'}")
#     print("-" * 70)
    
#     for m in range(8, 30):
#         prev_fail = None
#         prev_r2 = None
#         n_plateau = None
        
#         for n in range(4, 25):
#             fail = get_failure_exp(m, n)
#             r2 = renyi_per_sample(n)
            
#             if prev_fail is not None:
#                 if abs(fail - prev_fail) < 0.1 and abs(r2 - prev_r2) < 0.0001:
#                     if n_plateau is None:
#                         n_plateau = n
#                         e_pm2 = expected_pm2(n, m)
#                         print(f"{m:<6} {n_plateau:<12} {e_pm2:<22.4f} {fail:<20.1f} {r2:.6f}")
#                         break
            
#             prev_fail = fail
#             prev_r2 = r2
        
#         if n_plateau is None:
#             print(f"{m:<6} {'not plateaued':<12}")

# if __name__ == "__main__":
    
#     # static Rényi table
#     print("Rényi divergence vs n at m=24:")
#     renyi_static_table()
#     print()
    
#     # plateau analysis for selected dimensions
#     print("Plateau analysis:")
#     for m in [8, 14, 19, 24, 29]:
#         plateau_table(m)
#     print()
    
#     # plateau summary
#     print("Plateau summary across all dimensions:")
#     plateau_summary()