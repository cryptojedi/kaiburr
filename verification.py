# import random
# import sys

# def sample_fn(n_param, degree=256):
#     """Sample one polynomial from f(n)"""
#     coeffs = []
#     for _ in range(degree):
#         a = [random.randint(0,1) for _ in range(n_param)]
#         sign = 2*a[n_param-1] - 1
#         magnitude = (1 - a[0]) + 2*int(all(a[i]==1 for i in range(n_param-1)))
#         coeffs.append(sign * magnitude)
#     return coeffs

# def poly_mul_ntt(a, b, q=3329, n=256):
#     """Negacyclic polynomial multiplication mod (x^n+1, q)"""
#     result = [0] * n
#     for i in range(n):
#         for j in range(n):
#             idx = (i + j) % n
#             sign = -1 if (i + j) >= n else 1
#             result[idx] = (result[idx] + sign * a[i] * b[j]) % q
#     return result

# def poly_add(a, b, q=3329):
#     return [(x + y) % q for x, y in zip(a, b)]

# def poly_sub(a, b, q=3329):
#     return [(x - y) % q for x, y in zip(a, b)]

# def encode_message(bit, q=3329, n=256):
#     """Encode a single bit as a polynomial"""
#     val = q // 2 if bit else 0
#     return [val] + [0] * (n-1)

# def decode_message(poly, q=3329):
#     """Decode polynomial to bit"""
#     # check if first coefficient is closer to q/2 or 0
#     v = poly[0] % q
#     return 1 if min(v, q-v) > q//4 else 0

# def run_trial(m, n_fn, rq2, q=3329, n=256):
#     """Run one encryption/decryption and return True if failure"""
#     # key generation
#     # A is a random m x m matrix of polynomials
#     A = [[[ random.randint(0, q-1) for _ in range(n)] 
#            for _ in range(m)] for _ in range(m)]
#     s = [sample_fn(n_fn) for _ in range(m)]
#     e = [sample_fn(n_fn) for _ in range(m)]
    
#     # pk = As + e
#     pk = []
#     for i in range(m):
#         row_sum = [0]*n
#         for j in range(m):
#             prod = poly_mul_ntt(A[i][j], s[j], q, n)
#             row_sum = poly_add(row_sum, prod, q)
#         pk.append(poly_add(row_sum, e[i], q))
    
#     # encryption
#     msg_bit = random.randint(0, 1)
#     r = [sample_fn(n_fn) for _ in range(m)]
#     e1 = [sample_fn(n_fn) for _ in range(m)]
#     e2 = sample_fn(n_fn)
    
#     # u = A^T r + e1
#     u = []
#     for i in range(m):
#         col_sum = [0]*n
#         for j in range(m):
#             prod = poly_mul_ntt(A[j][i], r[j], q, n)
#             col_sum = poly_add(col_sum, prod, q)
#         u.append(poly_add(col_sum, e1[i], q))
    
#     # v = pk^T r + e2 + encode(msg)
#     v = [0]*n
#     for i in range(m):
#         prod = poly_mul_ntt(pk[i], r[i], q, n)
#         v = poly_add(v, prod, q)
#     v = poly_add(v, e2, q)
#     msg_poly = encode_message(msg_bit, q, n)
#     v = poly_add(v, msg_poly, q)
    
#     # compression on v
#     v = [int(round(x * rq2 / q)) % rq2 for x in v]
#     v = [int(round(x * q / rq2)) % q for x in v]
    
#     # decryption: v - s^T u
#     su = [0]*n
#     for i in range(m):
#         prod = poly_mul_ntt(s[i], u[i], q, n)
#         su = poly_add(su, prod, q)
    
#     decrypted_poly = poly_sub(v, su, q)
#     decrypted_bit = decode_message(decrypted_poly, q)
    
#     return decrypted_bit != msg_bit

# # run trials
# m, n_fn, rq2 = 82, 4, 12  # f(4) m=24 rq2=2^2
# num_trials = 10000
# failures = sum(run_trial(m, n_fn, rq2) for _ in range(num_trials))

# print(f"Parameters: m={m}, f({n_fn}), rq2=2^{int(rq2**0.5)}")
# print(f"Trials: {num_trials}")
# print(f"Failures: {failures}")
# print(f"Empirical failure rate: 2^{failures/num_trials:.1f}" if failures > 0 
#       else "No failures observed")