# Kaiburr: ML-KEM at (much) higher security

This repository contains all code and supplementary materials for our paper "Kaiburr: ML-KEM at (much) higher
security." We include the parameter analysis scripts, verified decryption-failure bounds, lattice estimates, C, Jasmin
and ACC implementations, benchmarks, and paper source.

## Platform

The analysis scripts, the lattice estimator, the C reference implementation and the paper run on any
platform. The Jasmin implementation compiles to x86-64 assembly, so it needs an x86-64 CPU, and its AVX2
builds, the C AVX2 implementation and the Intel benchmarks also need AVX2. The benchmarks also need Linux.
The toolchain setup for the formally verified bounds downloads Linux x86-64 binaries (opam, Z3, CVC4), it needs Linux on x86-64. For the ACC, see Pavona's toolchain guide linked from
[src/README.md](src/README.md#kaiburr-on-pavonas-acc).

## Cloning

This repo uses git submodules for the paper bibliography (`cryptobib`), the bounds and estimator, and the
implementations under `src/`. Clone recursively:

```bash
git clone --recurse-submodules https://github.com/cryptojedi/kaiburr.git
# if already cloned without --recurse-submodules:
git submodule update --init --recursive
```

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

### Analysis (Tables 1, 2, 4, 5)

Requires Python 3 (standard library only). See [analysis/README.md](analysis/README.md) for more.

```bash
cd analysis
python3 kaiburr.py
```

This first prints the Script column and sizes of Table 1, then Table 2 (its Kaiburr rows are also the Core-SVP
and size columns of Table 4), then Table 5.

### C implementation (Section 6.4)

Round-trip tests:

```bash
cd src/kaiburr-c/ref
make test/test_kaiburr1792 test/test_kaiburr4608 test/test_kaiburr6144
./test/test_kaiburr1792 && ./test/test_kaiburr4608 && ./test/test_kaiburr6144
```

and likewise in `src/kaiburr-c/avx2`.

### Lattice estimates (Tables 3, 4)

This requires SageMath. See [kaiburr-lattice-estimator/README.md](https://github.com/swechchhaad/kaiburr-lattice-estimator/blob/main/README.md) for details.

```bash
cd kaiburr-lattice-estimator
sage kaiburr.py    # Kaiburr-1792, -4608, -6144 (Tables 3 and 4)
sage frodo.py      # FrodoKEM-640, -976, -1344 (Table 4)
```

### Jasmin implementation (Section 6.4)

This requires the Jasmin compiler (`jasminc` and `jasmin-ct`, release `v2026.03.1`) on the `PATH`, or `JASMIN`
set to the directory that contains them. Please see the
[Jasmin installation guide](https://jasmin-lang.readthedocs.io/en/latest/misc/installation_guide.html) on how
to install the Jasmin compiler. We recommend using nix.

For constant-time checks, run in each `src/kaiburr-jasmin/code/jasmin/<kaiburr1792|kaiburr4608|kaiburr6144>/<ref|avx2>/`:

```bash
make ct     # all six builds
make sct    # AVX2 builds only
```

We further cross-check the Jasmin implementation against the C implementation:

```bash
cd src/kaiburr-jasmin
for p in kaiburr1792 kaiburr4608 kaiburr6144; do for i in ref avx2; do make -C code/jasmin/$p/$i jkem.s; done; done
make -C tests/apitest all_run_test_kem
```

### Intel benchmarks (Tables 8–10)

All our benchmarks require Linux on x86-64 with AVX2, GCC, CMake (for HQC) and `jasminc` on the `PATH` (please see the
[Jasmin installation guide](https://jasmin-lang.readthedocs.io/en/latest/misc/installation_guide.html)). All targets can be found at [src/benchmarks/BENCHMARK_SETUP.md](src/benchmarks/BENCHMARK_SETUP.md).

```bash
cd src/benchmarks
make run
```

For the paper we used GCC 12.2.0 with the Makefile's default flags (`-O3 -march=native -fomit-frame-pointer`)
and Hyper-Threading and Turbo Boost disabled, on an Intel Core i7-6700K (Skylake, Table 8), i7-8700K (Coffee
Lake, Table 9) and i9-13900K (Raptor Lake, Table 10). On the Raptor Lake, we pinned the benchmark to a
performance core. If GCC 12.2.0 is not your default compiler, select it with, e.g., `make CC=gcc-12 run`.
Cycle counts will differ on other CPUs and configurations.

### Formally verified bounds (Tables 1, 6)

See [kaiburr-bounds/README.md](https://github.com/swechchhaad/kaiburr-bounds/blob/main/README.md) for details on how to build this. Then

```bash
cd kaiburr-bounds
make check
```

checks the proofs, runs the bound calculator, and compares each bound admitted in the proofs with the
calculator output.

### ACC (Tables 11, 12)

Please see [src/README.md](src/README.md#kaiburr-on-pavonas-acc).

## Building the paper

To access the current version of the paper:

```bash
cd paper && make
```

## Building the poster / proposal

```bash
cd poster/proposal && make
```
