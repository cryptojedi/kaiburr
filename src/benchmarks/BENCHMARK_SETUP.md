# One Benchmark Setup for FrodoKEM, HQC and Kaiburr

All three KEMs are benchmarked by one program: `src/benchmarks/src/crypto_kem.c`.
Every binary in `src/benchmarks/bin/`
is this driver, compiled with the same flags, using the same cycle counter,
the same statistics and the same entropy source; the only thing that varies
between rows of the output table is which KEM is being called.

Run everything with:

```bash
cd src/benchmarks
make run
```
or to pin it to a single core:
```bash
taskset -c 2 make run
```

## Targets

```bash
make smoke                # everything at TIMINGS=101 RUNS=1
make run                  # everything

make run-kaiburr          # kaiburr4/6/8, C and Jasmin, ref and avx2
make run-kaiburr-c        # kaiburr4/6/8, C only
make run-kaiburr-jasmin   # kaiburr4/6/8, Jasmin only
make run-hqc              # hqc-1/3/5, ref and avx2
make run-frodo            # FrodoKEM-640 SHAKE, ref and avx2

make compile              # build without running
make clean
make help
```

## Legacy path

`src/benchmarks/fn/run_ab.sh` (`cd src/benchmarks/fn && make run`) is a
Kaiburr-only script that does pretty much the same thing.