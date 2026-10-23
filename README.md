# Kaiburr: ML-KEM at (much) higher security

This repository contains all code and supplementary materials for our paper "Kaiburr: ML-KEM at (much) higher
security." We include the parameter analysis scripts, verified decryption-failure bounds, lattice estimates, C, Jasmin
and ACC implementations, benchmarks, and paper source.

## Cloning

This repo uses git submodules for the paper bibliography (`cryptobib`), the bounds and estimator, and the
implementations under `src/`. Clone recursively and enter the repository:

```bash
git clone --recurse-submodules https://github.com/cryptojedi/kaiburr.git
cd kaiburr
```

**All commands in this README are run from this `kaiburr/` directory (the repository root).** Each command block
below starts with its own `cd`, so go back to `kaiburr/` before running the next block.

## Structure

```
analysis/                     failure probability, Core-SVP security, sizes
kaiburr-bounds/               EasyCrypt proofs of the decryption-failure bounds, OCaml bound calculator (submodule)
kaiburr-lattice-estimator/    lattice estimator for Kaiburr (submodule)
src/
  kaiburr-c/                  C implementation (ref, avx2), forked from Kyber (pq-crystals) (submodule)
  kaiburr-jasmin/             Jasmin implementation (ref, avx2), forked from formosa-mlkem (submodule)
  kaiburr-acc/                ACC implementation, forked from Pavona (submodule)
  benchmarks/                 common benchmark driver for Kaiburr, ML-KEM, FrodoKEM and HQC
  kyber-c/                    ML-KEM (Kyber) C code, for comparison (submodule)
  PQCrypto-LWEKE/             FrodoKEM code, for comparison
  hqc-next-release/           HQC code, for comparison
paper/                        LaTeX source of the paper
poster/                       poster and proposal
```

## Prerequisites

The analysis scripts, the lattice estimator, the C reference implementation and the paper run on any
platform. The Jasmin implementation compiles to x86-64 assembly, so it needs an x86-64 CPU, and its AVX2
builds, the C AVX2 implementation and the Intel benchmarks also need AVX2. The benchmarks also need Linux.
The toolchain setup for the formally verified bounds downloads Linux x86-64 binaries (opam, Z3, CVC4), so it
needs Linux on x86-64.

You only need the tools for the parts you want to reproduce:

| Tool | Needed for | How to install |
|---|---|---|
| Python 3 (standard library only) | [Analysis](#analysis-tables-1-2-4-5), [bounds](#formally-verified-bounds-tables-1-6) check | `sudo apt install python3` (Debian/Ubuntu) |
| C compiler (GCC or Clang) and GNU make | [C](#c-implementation-section-64), [Jasmin](#jasmin-implementation-section-64) | `sudo apt install build-essential` (Debian/Ubuntu) |
| SageMath | [Lattice estimates](#lattice-estimates-tables-3-4) | [SageMath installation guide](https://doc.sagemath.org/html/en/installation/index.html) |
| Jasmin compiler `v2026.03.1` (`jasminc`, `jasmin-ct`) | [Jasmin](#jasmin-implementation-section-64), [benchmarks](#intel-benchmarks-tables-810) | [Jasmin installation guide](https://jasmin-lang.readthedocs.io/en/latest/misc/installation_guide.html) (we recommend nix) |
| GCC 12.2.0, CMake | [Benchmarks](#intel-benchmarks-tables-810) | `sudo apt install gcc-12 cmake` (Debian/Ubuntu) |
| EasyCrypt `r2025.02`, OCaml 4.14.2, MPFR ≥ 4.2.1, Alt-Ergo 2.4.2, CVC4 1.8, Z3 4.8.17 | [Bounds](#formally-verified-bounds-tables-1-6) | step-by-step in [kaiburr-bounds/README.md](https://github.com/swechchhaad/kaiburr-bounds/blob/main/README.md#one-time-setup) |
| Pavona toolchain (Bazel via `bazelisk`) | [ACC](#acc-tables-11-12) | Pavona's [getting-started guide](https://github.com/pavona/pavona/blob/main/doc/getting_started/README.md) |
| XeLaTeX and BibTeX (e.g. TeX Live) | [Paper](#building-the-paper) | `sudo apt install texlive-full` (Debian/Ubuntu) |

## Where each result comes from

| Paper | Code |
|---|---|
| Table 1, warmup | `analysis/` (*Script* column, sizes), `kaiburr-bounds/` (*Machine-checked* column) |
| Table 2, parameter selection | `analysis/` |
| Table 3, lattice-estimator costs | `kaiburr-lattice-estimator/` |
| Table 4, comparison with FrodoKEM and HQC | `analysis/` (Kaiburr sizes, Core-SVP), `kaiburr-lattice-estimator/` (estimator column) |
| Table 5, failure probability under $f(\infty)$ | `analysis/` |
| Table 6, verified failure bounds | `kaiburr-bounds/` |
| Section 6.4, CT/SCT checks and testing | `src/kaiburr-c/`, `src/kaiburr-jasmin/`, `src/kaiburr-acc/` |
| Tables 8–10, Intel benchmarks | `src/benchmarks/` |
| Tables 11–12, ACC cycle counts and profile | `src/kaiburr-acc/` |

The FrodoKEM and HQC sizes and the HQC security categories in Table 4 are taken from their specifications; we provide the security estimates for FrodoKEM given by the lattice estimator.

## Running

We measured the running times below on two machines:

- **Apple M1** (8 cores, 8 GB RAM), macOS, Python 3.13.7: analysis and C implementation.
- **AMD Ryzen Threadripper PRO 7995WX** (96 cores, 191 GiB RAM), Debian 12 (kernel 6.1): all other sections.

### Analysis (Tables 1, 2, 4, 5)

**Goal.** `kaiburr.py` uses the Kyber team's scripts to compute the decryption-failure probability, the classical
and quantum Core-SVP security and the public-key and ciphertext sizes for ML-KEM with $n = 256$, $q = 3329$ and
no ciphertext compression, for the module ranks $k$ and noise distributions $f(t)$ we consider. These are the
numbers we used to select the three Kaiburr parameter sets. See [analysis/README.md](analysis/README.md) for more.

Requires Python 3 (standard library only). From the repository root:

```bash
cd analysis
python3 kaiburr.py
```

**Expected output.** The script prints three tables, one after the other. Failure probabilities are printed as
$\log_2$ values (`2^-133.7`), sizes in bytes.

1. `Warmup` (Table 1, *Script* column and sizes): ML-KEM's original $\mathrm{CBD}_2$ noise at $k = 3, \dots, 8$.
   This shows that only increasing $k$ quickly breaks the $2^{-128}$ failure bound.
2. `Parameter selection` (Table 2; its Kaiburr rows are also the Core-SVP and size columns of Table 4): for
   each noise $f(t)$, the largest $k$ that keeps the failure probability below $2^{-128}$ and the sizes within
   FrodoKEM-640's budget, with its Core-SVP security.
3. `Ceiling` (Table 5): the failure probability under the limiting distribution $f(\infty)$, which shows that
   $k = 29$ is the largest rank possible in this family.

You should see these values:

| `Warmup` $k$ | failure | pk | ct |
|---|---|---|---|
| 3 | 2^-299.6 | 1184 | 1536 |
| 4 | 2^-231.1 | 1568 | 1920 |
| 5 | 2^-186.5 | 1952 | 2304 |
| 6 | 2^-155.9 | 2336 | 2688 |
| 7 | 2^-133.7 | 2720 | 3072 |
| 8 | 2^-116.8 | 3104 | 3456 |

| `Parameter selection` scheme | $k$ | noise | failure | class. | quant. | pk | ct |
|---|---|---|---|---|---|---|---|
| Kaiburr-256  | 1  | f(2) | 2^-159.1 | 52   | 47   | 416  | 768  |
| Kaiburr-768  | 3  | f(3) | 2^-139.3 | 191  | 174  | 1184 | 1536 |
| **Kaiburr-1792** | 7  | f(4) | 2^-133.7 | 479  | 434  | 2720 | 3072 |
| Kaiburr-3328 | 13 | f(5) | 2^-128.4 | 918  | 832  | 5024 | 5376 |
| **Kaiburr-4608** | 18 | f(6) | 2^-134.1 | 1281 | 1162 | 6944 | 7296 |
| Kaiburr-5888 | 23 | f(7) | 2^-129.8 | 1650 | 1497 | 8864 | 9216 |
| **Kaiburr-6144** | 24 | f(8) | 2^-139.9 | 1717 | 1557 | 9248 | 9600 |

The rows in bold are the selected Kaiburr parameter sets.

| `Ceiling` $k$ | failure | pk | ct |
|---|---|---|---|
| 24 | 2^-158.7 | 9248  | 9600  |
| 26 | 2^-146.2 | 10016 | 10368 |
| 28 | 2^-135.5 | 10784 | 11136 |
| 29 | 2^-130.6 | 11168 | 11520 |
| 30 | 2^-126.1 | 11552 | 11904 |

**Running time.** `Warmup` and `Ceiling` take seconds. `Parameter selection` takes several hours, because it
runs the Core-SVP attack search for every row, and the larger rows take longest. Its rows are printed one at a
time as they finish.

### C implementation (Section 6.4)

**Goal.** Round-trip tests for the C implementation of the three Kaiburr parameter sets. For each, the test
runs 1000 iterations of key generation, encapsulation and decapsulation and checks that both sides agree on the
shared secret. It also checks that decapsulation with an invalid secret key or a modified ciphertext gives a
different shared secret.

From the repository root:

```bash
cd src/kaiburr-c
for i in ref avx2; do
  echo "== $i =="
  make -C $i test/test_kaiburr1792 test/test_kaiburr4608 test/test_kaiburr6144
  for p in 1792 4608 6144; do ./$i/test/test_kaiburr$p || echo "test_kaiburr$p FAILED"; done
done
```

The `avx2` builds need an x86-64 CPU with AVX2; on other platforms, replace `ref avx2` with `ref`.

**Expected output.** Each test prints nothing while it runs. If all iterations succeed, it prints the key and
ciphertext sizes in bytes:

| Parameter set | `CRYPTO_SECRETKEYBYTES` | `CRYPTO_PUBLICKEYBYTES` | `CRYPTO_CIPHERTEXTBYTES` |
|---|---|---|---|
| Kaiburr-1792 | 5472  | 2720 | 3072 |
| Kaiburr-4608 | 13920 | 6944 | 7296 |
| Kaiburr-6144 | 18528 | 9248 | 9600 |

The output is the same for `ref` and `avx2`. If a test fails, it prints `ERROR keys`, `ERROR invalid sk` or
`ERROR invalid ciphertext` and exits with status 1.

**Running time.** For the `ref` implementation, about 3 s (Kaiburr-1792), 12 s (Kaiburr-4608) and 20 s
(Kaiburr-6144) of CPU time on our machine.

### Lattice estimates (Tables 3, 4)

**Goal.** Runs our fork of the [lattice estimator](https://github.com/malb/lattice-estimator) against all
eight attacks it supports, for Kaiburr and, for comparison, FrodoKEM.

This requires SageMath. See [kaiburr-lattice-estimator/README.md](https://github.com/swechchhaad/kaiburr-lattice-estimator/blob/main/README.md) for details.
From the repository root:

```bash
cd kaiburr-lattice-estimator
sage kaiburr.py    # Kaiburr-1792, -4608, -6144 (Tables 3 and 4)
sage frodo.py      # FrodoKEM-640, -976, -1344 (Table 4)
```

**Expected output.** For each parameter set, the script prints the parameters (`LWEParameters(...)`) and then
one line per attack, such as

```
usvp                 :: rop: ≈2^494.0, red: ≈2^494.0, δ: 1.001388, β: 1651, d: 3168, tag: usvp
```

where `rop` is the $\log_2$ cost of the attack in Table 3. The estimator prints only attacks with a finite
cost, and prints `bdd_hybrid` and `bdd_mitm_hybrid` only if they are cheaper than `bdd` and `bdd_hybrid`
respectively. So for each set you will see lines for `usvp`, `bdd`, `dual` (except Kaiburr-6144) and
`dual_hybrid`, but not for `bdd_hybrid`, `bdd_mitm_hybrid` or `arora-gb`. Attacks that crash are reported as
`Algorithm ... failed with ...`. This is expected for `CodedBKW` (`bkw`) on all three sets (`Calling ceil() on
infinity or NaN`) and for `dual` on Kaiburr-6144 (`Numerical result out of range`).

The printed costs should match Table 3 of the paper:

| Attack | Kaiburr-1792 | Kaiburr-4608 | Kaiburr-6144 |
|---|---|---|---|
| `usvp`            | 494.0     | 1275.5     | 1701.0     |
| `bdd`             | 488.7     | **1268.9** | **1694.3** |
| `bdd_hybrid`      | 488.7 (not printed) | 1268.9 (not printed) | 1694.3 (not printed) |
| `bdd_mitm_hybrid` | 883.0 (not printed) | 2411.1 (not printed) | 3265.2 (not printed) |
| `dual`            | 519.8     | 1400.8     | fails      |
| `dual_hybrid`     | **467.3** | 1458.3     | 2120.4     |
| `bkw`             | fails     | fails      | fails      |
| `arora-gb`        | ∞ (not printed) | ∞ (not printed) | ∞ (not printed) |

Bold marks the cheapest attack for each set. For `frodo.py`, the cheapest attacks cost $2^{162.9}$
(FrodoKEM-640), $2^{225.2}$ (FrodoKEM-976) and $2^{281.7}$ (FrodoKEM-1344).

**Running time.** About 2 minutes for `kaiburr.py` and under 1 minute for `frodo.py` on the
Threadripper. Both use at most 8 cores, so a machine with 8 cores should take about as long.

### Jasmin implementation (Section 6.4)

This requires the Jasmin compiler (`jasminc` and `jasmin-ct`, release `v2026.03.1`) on the `PATH`, or `JASMIN`
set to the directory that contains them. Please see the
[Jasmin installation guide](https://jasmin-lang.readthedocs.io/en/latest/misc/installation_guide.html) on how
to install the Jasmin compiler. We recommend using nix. It also needs an x86-64 CPU, with AVX2 for the `avx2`
builds.

**Please note that you need release `v2026.03.1` or newer to run these tests; older releases will not work.** Installing through nixpkgs
(`nix-env -iA nixpkgs.jasmin-compiler.bin`) may give you an older release, so we recommend building the release
from its tarball instead:

```bash
mkdir -p ~/tools && cd ~/tools
curl -LO https://github.com/jasmin-lang/jasmin/releases/download/v2026.03.1/jasmin-compiler-v2026.03.1.tar.bz2
tar xjf jasmin-compiler-v2026.03.1.tar.bz2
cd jasmin-compiler-v2026.03.1
nix-shell compiler/ --run 'make -C compiler'
export JASMIN=$HOME/tools/jasmin-compiler-v2026.03.1/compiler
$JASMIN/jasminc -version    # should print 2026.03.1
```

#### Constant-time checks

**Goal.** `jasmin-ct` checks that each of the six builds (three parameter sets, `ref` and `avx2`) is constant
time, i.e., that no branch or memory address depends on secret data. For the AVX2 builds, it also checks
speculative constant time (SCT), i.e., that this still holds under Spectre-v1-style speculative execution.

From the repository root:

```bash
cd src/kaiburr-jasmin/code/jasmin
for p in kaiburr1792 kaiburr4608 kaiburr6144; do
  for i in ref avx2; do make -s -C $p/$i ct  >/dev/null 2>&1 && echo "CT  $p/$i: PASS" || echo "CT  $p/$i: FAIL"; done
  make -s -C $p/avx2 sct >/dev/null 2>&1 && echo "SCT $p/avx2: PASS" || echo "SCT $p/avx2: FAIL"
done
```

**Expected output.**

```
CT  kaiburr1792/ref: PASS
CT  kaiburr1792/avx2: PASS
SCT kaiburr1792/avx2: PASS
CT  kaiburr4608/ref: PASS
CT  kaiburr4608/avx2: PASS
SCT kaiburr4608/avx2: PASS
CT  kaiburr6144/ref: PASS
CT  kaiburr6144/avx2: PASS
SCT kaiburr6144/avx2: PASS
```

**Running time.** A few seconds for all nine checks on the Threadripper.

#### Cross-check against the C implementation

**Goal.** Compiles each of the six Jasmin builds to assembly (`jkem.s`) and links it with a test that runs
10,000 random round trips. Each round trip runs key generation, encapsulation and decapsulation, with the same
randomness, in both the Jasmin and the C implementation and checks that keys, ciphertexts and shared secrets
are byte-for-byte equal. It then corrupts one byte of the ciphertext and checks that both implementations
return the same (implicit-rejection) shared secret.

From the repository root:

```bash
cd src/kaiburr-jasmin
for p in kaiburr1792 kaiburr4608 kaiburr6144; do for i in ref avx2; do make -C code/jasmin/$p/$i jkem.s; done; done
make -C tests/apitest all_run_test_kem
```

**Expected output.** First, make runs `jasminc` for each of the six builds. Then six test binaries are built and
run in this order: `test_kem_avx2_kaiburr1792`, `test_kem_avx2_kaiburr4608`, `test_kem_avx2_kaiburr6144`,
`test_kem_ref_kaiburr1792`, `test_kem_ref_kaiburr4608`, `test_kem_ref_kaiburr6144`. Each prints its progress,
ending with

```
Progress: 10000/10000 (100.0%)
```

The cross-check passes if all six reach `10000/10000` and make finishes without an error. On a mismatch, the
test prints which output differs (e.g. `crypto_kem_enc ct mismatch at byte 17`) and stops.

**Running time.** About 18 minutes on the Threadripper. The six tests run one after another on a single core.

### Intel benchmarks (Tables 8–10)

**Goal.** Measures the cycle counts of key generation, encapsulation and decapsulation for Kaiburr (C and
Jasmin, `ref` and `avx2`) and, on the same benchmark driver, ML-KEM, FrodoKEM and HQC.

All our benchmarks require Linux on x86-64 with AVX2, GCC, CMake (for HQC) and `jasminc` on the `PATH` (please see the
[Jasmin installation guide](https://jasmin-lang.readthedocs.io/en/latest/misc/installation_guide.html)). All targets can be found at [src/benchmarks/BENCHMARK_SETUP.md](src/benchmarks/BENCHMARK_SETUP.md).
From the repository root:

```bash
cd src/benchmarks
make run
```

For a quick check that everything builds and runs, use `make smoke` instead, which takes fewer measurements.

For the paper we used GCC 12.2.0 with the Makefile's default flags (`-O3 -march=native -fomit-frame-pointer`)
and Hyper-Threading and Turbo Boost disabled, on an Intel Core i7-6700K (Skylake, Table 8), i7-8700K (Coffee
Lake, Table 9) and i9-13900K (Raptor Lake, Table 10). On the Raptor Lake, we pinned the benchmark to a
performance core. If GCC 12.2.0 is not your default compiler, select it with, e.g., `make CC=gcc-12 run`.

**Expected output.** A single Markdown table, built up one row at a time, with one row per KEM and
implementation. Each cell gives the median cycle count and the quartiles, as `median (Q1-Q3)`, for `keypair`,
`keypair_derand`, `enc`, `enc_derand` and `dec` (`n/a` where an implementation has no derandomized API). The
`keypair`, `enc` and `dec` columns are the KeyGen, Enc and Dec columns of Tables 8–10. Cycle counts will differ on
other CPUs and configurations, so compare the relative order of the schemes rather than the absolute numbers.

**Running time.** Several hours, depending on the machine.

### Formally verified bounds (Tables 1, 6)

**Goal.** Checks the EasyCrypt proofs that the decryption-failure probability of each Kaiburr parameter set
(and of the warmup parameter sets of Table 1) is at most the bound in Tables 1 and 6. The proofs assume a numeric
tail bound; an OCaml calculator computes it, and a script checks that each computed tail is below the bound the
proofs assume.

See [kaiburr-bounds/README.md](https://github.com/swechchhaad/kaiburr-bounds/blob/main/README.md) for details on how to set up the toolchain. Then, from the repository root:

```bash
cd kaiburr-bounds
make check
```

**Expected output.** First, EasyCrypt checks the 24 proof files (`[✓] [0024/0024] ...`). Then the calculator
prints the computed bound for each parameter set, and finally the check prints:

```
parameter set    k noise   admitted    computed  result
kaiburr-1792     7  f(4)     2^-133  2^-133.3422  ok
kaiburr-4608    18  f(6)     2^-133  2^-133.8111  ok
kaiburr-6144    24  f(8)     2^-139  2^-139.5815  ok
warmup-k3        3  CBD2     2^-300  2^-300.9812  ok
warmup-k4        4  CBD2     2^-230  2^-230.5887  ok
warmup-k5        5  CBD2     2^-186  2^-186.1013  ok
warmup-k6        6  CBD2     2^-155  2^-155.5587  ok
warmup-k7        7  CBD2     2^-133  2^-133.3422  ok
warmup-k8        8  CBD2     2^-116  2^-116.4773  ok
all admitted bounds are backed by the calculator
```

The *admitted* column is the *Machine-checked* column of Table 1 and the *Verified bound* column of Table 6. The
full expected output is in [kaiburr-bounds/README.md](https://github.com/swechchhaad/kaiburr-bounds/blob/main/README.md#running).

**Running time.** About 3 minutes on the Threadripper with the default `JOBS=4`: under 2 minutes for the
proofs, the rest for building and running the calculator.

### ACC (Tables 11, 12)

Please see [src/README.md](src/README.md#kaiburr-on-pavonas-acc).

## Building the paper

To build the current version of the paper (`paper/kaiburr.pdf`), from the repository root:

```bash
cd paper && make
```

## Building the poster / proposal

From the repository root:

```bash
cd poster/proposal && make
```
