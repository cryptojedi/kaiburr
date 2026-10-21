# Benchmarks

Kaiburr, ML-KEM, FrodoKEM and HQC are all benchmarked with one driver, `src/benchmarks/src/crypto_kem.c`.
Each binary in `src/benchmarks/bin/` is that driver built with the same flags, cycle counter, statistics
and entropy source; only the KEM it calls differs.

Run everything:

```bash
cd src/benchmarks
make run
```
or pinned to one core:
```bash
taskset -c 2 make run
```

## Targets

```bash
make smoke                # everything at TIMINGS=101 RUNS=1
make run                  # everything

make run-kaiburr          # Kaiburr-1792/4608/6144, C and Jasmin, ref and avx2
make run-kaiburr-c        # Kaiburr-1792/4608/6144, C only
make run-kaiburr-jasmin   # Kaiburr-1792/4608/6144, Jasmin only
make run-mlkem            # ML-KEM-512/768/1024, C, ref and avx2
make run-mlkem-jasmin     # ML-KEM-768/1024, Jasmin, ref and avx2
make run-hqc              # hqc-1/3/5, ref and avx2
make run-frodo            # FrodoKEM-640/976/1344, AES and SHAKE, ref and avx2

make compile              # build without running
make clean
make help
```

The ML-KEM Jasmin baseline (formosa-mlkem commit `475b874`) is extracted from the git history of `src/kaiburr-jasmin`, which is forked from formosa-mlkem. This needs a full clone of that submodule,
which `git submodule update --init --recursive` gives by default.

## Legacy path

`src/benchmarks/fn/run_ab.sh` (`cd src/benchmarks/fn && make run`) is an older, Kaiburr-only script that
does much the same thing.
