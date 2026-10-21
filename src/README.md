# Implementations

In this folder, we give all Kaiburr implementations. `kaiburr-c`, `kaiburr-jasmin`,
`kaiburr-acc` and `kyber-c` are separate repositories, included here as git submodules. Initialize them
from the repo root:

```bash
git submodule update --init --recursive src
```

```
kaiburr-c/          C implementation (ref, avx2), forked from Kyber (pq-crystals) at commit 4768bd3
kaiburr-jasmin/     Jasmin implementation (ref, avx2), forked from formosa-mlkem at commit 475b874
kaiburr-acc/        ACC implementation, forked from Pavona at commit 07ccb24
benchmarks/         common benchmark driver for Kaiburr, ML-KEM, FrodoKEM and HQC
kyber-c/            ML-KEM (Kyber) C code, for comparison on the same benchmark harness
PQCrypto-LWEKE/     FrodoKEM code, for comparison
hqc-next-release/   HQC code, for comparison
```

Please see the top-level [README](../README.md#running) for how to test and benchmark the C and Jasmin
implementations, and [benchmarks/BENCHMARK_SETUP.md](benchmarks/BENCHMARK_SETUP.md) for the benchmark
targets.

## Kaiburr on Pavona's ACC

`kaiburr-acc` is Pavona (<https://github.com/pavona/pavona>) at commit `07ccb24` with the Kaiburr ACC
implementation added. The Kaiburr changes are in:

- `sw/acc/crypto/mlkem/`: the Kaiburr ACC implementation
- `sw/acc/crypto/tests/mlkem/`: tests against a `kyber-py`-based Python model
  (`kaiburr_mlkem.py`), round-trip tests, and the benchmark targets
- `hw/ip/acc/`: the modified ACC hardware and its simulator statistics

The submodule's own `README.md` is Pavona's; see its
[getting-started guide](https://github.com/pavona/pavona/blob/main/doc/getting_started/README.md) for
the toolchain. All commands below should be run from `src/kaiburr-acc`.

### Benchmarks (Tables 11, 12)

The `*_bench_keygen`, `*_bench_keygen_encap` and `*_bench` targets run the round trip up to and including
KeyGen, Enc and Dec respectively, giving total cycle counts M1, M2 and M3. Then KeyGen = M1, Enc = M2 - M1
and Dec = M3 - M2.

```bash
./bazelisk.sh test --test_output=errors \
  //sw/acc/crypto/tests/mlkem:kaiburr{1792,4608,6144}_bench_keygen \
  //sw/acc/crypto/tests/mlkem:kaiburr{1792,4608,6144}_bench_keygen_encap \
  //sw/acc/crypto/tests/mlkem:kaiburr{1792,4608,6144}_bench
```

These results are for the modified ACC with 127 KiB of visible data memory (set in
`hw/ip/acc/data/acc.hjson`). The benchmarks use fixed all-zero randomness, and
the simulator is deterministic, so each count is exact.

Per-function cycle counts from a `_bench` log, which give the `poly_gen_matrix`, `basemul_acc` and noise
(`poly_getnoise`) columns of Table 12:

```bash
python3 hw/ip/acc/util/acc_profile.py bazel-testlogs/sw/acc/crypto/tests/mlkem/<name>/test.log
```

The same log also contains the simulator's per-instruction statistics for each function. The four middle
columns of Table 12 split the cycles of `poly_gen_matrix` by instruction class, as described in Section 7.2
of the paper.

### Tests

```bash
./bazelisk.sh test //sw/acc/crypto/tests/mlkem/...
```

runs all tests and benchmarks, including known-answer tests for keypair, encapsulation and decapsulation.
