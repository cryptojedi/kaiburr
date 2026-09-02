# Unified Benchmark Setup for FrodoKEM, HQC, and Kaiburr

Here we explain the unified benchmarking infrastructure that has been set up to measure all three KEM implementations (FrodoKEM, HQC, and Kaiburr) using the same methodology.

## Shared Infrastructure

All benchmarks use:

### CPU Cycle Measurement (`cpucycles.c`)
- **x86-64**: CPUID+RDTSC at start, RDTSCP+LFENCE at end (strictest serialization)
- **ARM/other**: CLOCK_MONOTONIC fallback (nanosecond precision)
- Provides: `cpucycles_begin()`, `cpucycles_end()`

### Configuration (`config.h`)
Configurable parameters:
- `RUNS`: Number of complete benchmark runs (default: 3)
- `TIMINGS`: Iterations per operation per run (default: 10001)
- `RUNS_SORT`: Sort results across runs before reporting (default: 1)

### Statistics (`cpucycles.c`)
Reports:
- **Median**: Robust central tendency (50th percentile)
- **Q1**: Lower quartile (25th percentile)
- **Q3**: Upper quartile (75th percentile)


## Kaiburr Benchmarks

### Location
`src/benchmarks/`

Kaiburr already has unified benchmarking set up. For reference:

```bash
cd src/benchmarks/fn
make run                 # Run all implementations
make ref                 # Reference only
make avx2                # AVX2 optimized only
``

## FrodoKEM Benchmarks

### Location
`src/PQCrypto-LWEKE/FrodoKEM/tests/`

```bash
cd src/PQCrypto-LWEKE/FrodoKEM

# Build and run FrodoKEM-640 benchmark
make benchmark640 ARCH=ARM USE_OPENSSL=FALSE

# Build and run FrodoKEM-976 benchmark
make benchmark976 ARCH=ARM USE_OPENSSL=FALSE

# Build and run FrodoKEM-1344 benchmark
make benchmark1344 ARCH=ARM USE_OPENSSL=FALSE

# Build and run all three benchmarks
make benchmark ARCH=ARM USE_OPENSSL=FALSE
```

## HQC Benchmarks

### Location
`src/hqc-next-release/tests/bench/`

First, configure and build HQC:
```bash
cd src/hqc-next-release
mkdir build
cd build
cmake ..
make
```

Then run benchmarks:
```bash
# Run HQC-1 benchmark
./tests/bench/benchmark_kem_unified_hqc_1

# Run HQC-3 benchmark
./tests/bench/benchmark_kem_unified_hqc_3

# Run HQC-5 benchmark
./tests/bench/benchmark_kem_unified_hqc_5
```