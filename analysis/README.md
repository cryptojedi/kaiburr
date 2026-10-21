# Part 1: Parameter analysis

This folder includes all decryption-failure probability and Core-SVP security scripts for Kaiburr. Most of the code has been adapted from the Kyber team's security and failure-probability scripts.

## Running

Requires Python 3 (standard library only).

```bash
python3 kaiburr.py
```

This prints three blocks for $n = 256$, $q = 3329$ and no compression:

| Block | Paper | Contents |
|---|---|---|
| `Warmup` | Table 1, *Script* column, pk and ct | Failure probability with $\mathrm{CBD}_2$ for $k = 3, \dots, 8$ |
| `Parameter selection` | Table 2; Kaiburr rows of Table 4 (Core-SVP, pk, ct) | Failure probability, classical and quantum Core-SVP, pk and ct for the seven $(t, k)$ pairs of Table 2 |
| `Ceiling` | Table 5 | Failure probability under $f(\infty)$ for $k = 24, 26, 28, 29, 30$ |

We note that the parameter-selection block could be very slow because it runs the Core-SVP attack search for every row.
Failure probabilities are printed in log2 form, e.g. `2^-133.7`.

