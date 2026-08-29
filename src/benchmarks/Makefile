CFLAGS ?= -Wall -O3 -fomit-frame-pointer -fno-lto -march=native

CPU ?= ""

# kaiburr-jasmin
KAIBURR_JASMIN := \
 bin/kaiburr4-jasmin-avx2 \
 bin/kaiburr6-jasmin-avx2 \
 bin/kaiburr8-jasmin-avx2

# kaiburr-c
KAIBURR_C := \
 bin/kaiburr-c-ref \
 bin/kaiburr-c-avx2

ALL := $(KAIBURR_JASMIN) $(KAIBURR_C)

.PHONY: compile compile-c compile-all run-jasmin run-c run
.PHONY: compile-frodokem-ref compile-frodokem-avx2 compile-frodokem
.PHONY: run-frodokem-ref run-frodokem-avx2 run-frodokem
.PHONY: compile-hqc-ref compile-hqc-avx2 compile-hqc
.PHONY: run-hqc-ref run-hqc-avx2 run-hqc
.PHONY: compile-pqc run-pqc
.PHONY: build-hqc-ref build-hqc-avx2

default: run-jasmin

compile: $(KAIBURR_JASMIN)
compile-c: $(KAIBURR_C)
compile-all: $(ALL)

run-jasmin: $(KAIBURR_JASMIN)
	@./bin/kaiburr4-jasmin-avx2 "$(CPU)" "kaiburr4-jasmin-avx2" 1
	@./bin/kaiburr6-jasmin-avx2 "$(CPU)" "kaiburr6-jasmin-avx2" 0
	@./bin/kaiburr8-jasmin-avx2 "$(CPU)" "kaiburr8-jasmin-avx2" 0

run-c: $(KAIBURR_C)
	@./bin/kaiburr-c-ref "$(CPU)" "kaiburr-c-ref" 1
	@./bin/kaiburr-c-avx2 "$(CPU)" "kaiburr-c-avx2" 0

run: run-jasmin run-c

#-- FrodoKEM benchmarks ------------------------------------------------

FRODOKEM_VARIANTS := frodo640 frodo976 frodo1344

# ref implementations
FRODOKEM_REF := $(addprefix bin/benchmark-,$(addsuffix -ref,$(FRODOKEM_VARIANTS)))

# avx2 implementations
FRODOKEM_AVX2 := $(addprefix bin/benchmark-,$(addsuffix -avx2,$(FRODOKEM_VARIANTS)))

compile-frodokem-ref: $(FRODOKEM_REF)
compile-frodokem-avx2: $(FRODOKEM_AVX2)
compile-frodokem: compile-frodokem-ref compile-frodokem-avx2

run-frodokem-ref: $(FRODOKEM_REF)
	@for f in $(FRODOKEM_REF); do echo "=== Running $$f ==="; $$f "$(CPU)" "$$(basename $$f)" 1; done

run-frodokem-avx2: $(FRODOKEM_AVX2)
	@for f in $(FRODOKEM_AVX2); do echo "=== Running $$f ==="; $$f "$(CPU)" "$$(basename $$f)" 0; done

run-frodokem: run-frodokem-ref run-frodokem-avx2

# FrodoKEM-640
bin/benchmark-frodo640-ref: randombytes/librandombytes1.a
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-D_AMD64_ -DNIX -D_REFERENCE_ -D_SHAKE128_FOR_A_ \
		-I../frodokem/src/ -Irandombytes/ \
		-DCRYPTO_SECRETKEYBYTES=CRYPTO_SECRETKEYBYTES_FRODO640 \
		-DCRYPTO_PUBLICKEYBYTES=CRYPTO_PUBLICKEYBYTES_FRODO640 \
		-DCRYPTO_CIPHERTEXTBYTES=CRYPTO_CIPHERTEXTBYTES_FRODO640 \
		-DCRYPTO_BYTES=CRYPTO_BYTES_FRODO640 \
		../frodokem/src/frodo640.c ../frodokem/src/util.c \
		../frodokem/common/sha3/fips202.c \
		randombytes/librandombytes1.a

bin/benchmark-frodo640-avx2: randombytes/librandombytes1.a
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-D_AMD64_ -DNIX -D_FAST_ -D_SHAKE128_FOR_A_ \
		-I../frodokem/src/ -Irandombytes/ \
		-DCRYPTO_SECRETKEYBYTES=CRYPTO_SECRETKEYBYTES_FRODO640 \
		-DCRYPTO_PUBLICKEYBYTES=CRYPTO_PUBLICKEYBYTES_FRODO640 \
		-DCRYPTO_CIPHERTEXTBYTES=CRYPTO_CIPHERTEXTBYTES_FRODO640 \
		-DCRYPTO_BYTES=CRYPTO_BYTES_FRODO640 \
		../frodokem/src/frodo640.c ../frodokem/src/util.c \
		../frodokem/common/sha3/fips202.c ../frodokem/common/sha3/fips202x4.c \
		randombytes/librandombytes1.a

# FrodoKEM-976
bin/benchmark-frodo976-ref: randombytes/librandombytes1.a
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-D_AMD64_ -DNIX -D_REFERENCE_ -D_SHAKE128_FOR_A_ \
		-I../frodokem/src/ -Irandombytes/ \
		-DCRYPTO_SECRETKEYBYTES=CRYPTO_SECRETKEYBYTES_FRODO976 \
		-DCRYPTO_PUBLICKEYBYTES=CRYPTO_PUBLICKEYBYTES_FRODO976 \
		-DCRYPTO_CIPHERTEXTBYTES=CRYPTO_CIPHERTEXTBYTES_FRODO976 \
		-DCRYPTO_BYTES=CRYPTO_BYTES_FRODO976 \
		../frodokem/src/frodo976.c ../frodokem/src/util.c \
		../frodokem/common/sha3/fips202.c \
		randombytes/librandombytes1.a

bin/benchmark-frodo976-avx2: randombytes/librandombytes1.a
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-D_AMD64_ -DNIX -D_FAST_ -D_SHAKE128_FOR_A_ \
		-I../frodokem/src/ -Irandombytes/ \
		-DCRYPTO_SECRETKEYBYTES=CRYPTO_SECRETKEYBYTES_FRODO976 \
		-DCRYPTO_PUBLICKEYBYTES=CRYPTO_PUBLICKEYBYTES_FRODO976 \
		-DCRYPTO_CIPHERTEXTBYTES=CRYPTO_CIPHERTEXTBYTES_FRODO976 \
		-DCRYPTO_BYTES=CRYPTO_BYTES_FRODO976 \
		../frodokem/src/frodo976.c ../frodokem/src/util.c \
		../frodokem/common/sha3/fips202.c ../frodokem/common/sha3/fips202x4.c \
		randombytes/librandombytes1.a

# FrodoKEM-1344
bin/benchmark-frodo1344-ref: randombytes/librandombytes1.a
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-D_AMD64_ -DNIX -D_REFERENCE_ -D_SHAKE128_FOR_A_ \
		-I../frodokem/src/ -Irandombytes/ \
		-DCRYPTO_SECRETKEYBYTES=CRYPTO_SECRETKEYBYTES_FRODO1344 \
		-DCRYPTO_PUBLICKEYBYTES=CRYPTO_PUBLICKEYBYTES_FRODO1344 \
		-DCRYPTO_CIPHERTEXTBYTES=CRYPTO_CIPHERTEXTBYTES_FRODO1344 \
		-DCRYPTO_BYTES=CRYPTO_BYTES_FRODO1344 \
		../frodokem/src/frodo1344.c ../frodokem/src/util.c \
		../frodokem/common/sha3/fips202.c \
		randombytes/librandombytes1.a

bin/benchmark-frodo1344-avx2: randombytes/librandombytes1.a
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-D_AMD64_ -DNIX -D_FAST_ -D_SHAKE128_FOR_A_ \
		-I../frodokem/src/ -Irandombytes/ \
		-DCRYPTO_SECRETKEYBYTES=CRYPTO_SECRETKEYBYTES_FRODO1344 \
		-DCRYPTO_PUBLICKEYBYTES=CRYPTO_PUBLICKEYBYTES_FRODO1344 \
		-DCRYPTO_CIPHERTEXTBYTES=CRYPTO_CIPHERTEXTBYTES_FRODO1344 \
		-DCRYPTO_BYTES=CRYPTO_BYTES_FRODO1344 \
		../frodokem/src/frodo1344.c ../frodokem/src/util.c \
		../frodokem/common/sha3/fips202.c ../frodokem/common/sha3/fips202x4.c \
		randombytes/librandombytes1.a

#-- HQC benchmarks ---------------------------------------------------

HQC_VARIANTS := hqc-1 hqc-3 hqc-5

# ref implementations
HQC_REF := $(addprefix bin/benchmark-,$(addsuffix -ref,$(HQC_VARIANTS)))

# avx2 implementations
HQC_AVX2 := $(addprefix bin/benchmark-,$(addsuffix -avx2,$(HQC_VARIANTS)))

compile-hqc-ref: build-hqc-ref $(HQC_REF)
compile-hqc-avx2: build-hqc-avx2 $(HQC_AVX2)
compile-hqc: compile-hqc-ref compile-hqc-avx2

run-hqc-ref: $(HQC_REF)
	@for f in $(HQC_REF); do echo "=== Running $$f ==="; $$f "$(CPU)" "$$(basename $$f)" 1; done

run-hqc-avx2: $(HQC_AVX2)
	@for f in $(HQC_AVX2); do echo "=== Running $$f ==="; $$f "$(CPU)" "$$(basename $$f)" 0; done

run-hqc: run-hqc-ref run-hqc-avx2

build-hqc-ref:
	mkdir -p build-hqc-ref && cd build-hqc-ref && \
	cmake -DHQC_ARCH=ref -DHQC_X86_IMPL=avx256 ../hqc 2>&1 | grep -v "^--" && \
	$(MAKE) hqc_1_ref hqc_3_ref hqc_5_ref 2>&1 | grep -v "Built target"

build-hqc-avx2:
	mkdir -p build-hqc-avx2 && cd build-hqc-avx2 && \
	cmake -DHQC_ARCH=x86_64 -DHQC_X86_IMPL=avx256 ../hqc 2>&1 | grep -v "^--" && \
	$(MAKE) hqc_1_x86_64 hqc_3_x86_64 hqc_5_x86_64 2>&1 | grep -v "Built target"

bin/benchmark-hqc-1-ref: build-hqc-ref randombytes/librandombytes1.a
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-I../hqc/src/common -I../hqc/src/common/hqc-1 -I../hqc/src/ref -I../hqc/src/ref/hqc-1 \
		-I../hqc/lib/fips202 -Ibuild-hqc-ref/src -Irandombytes/ \
		build-hqc-ref/src/CMakeFiles/hqc_1_ref.dir/common/*.c.o \
		build-hqc-ref/src/CMakeFiles/hqc_1_ref.dir/ref/*.c.o \
		build-hqc-ref/src/CMakeFiles/hqc_1_ref.dir/ref/hqc-1/*.c.o \
		build-hqc-ref/lib/CMakeFiles/fips202.dir/*.c.o \
		randombytes/librandombytes1.a

bin/benchmark-hqc-1-avx2: build-hqc-avx2 randombytes/librandombytes1.a
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-I../hqc/src/common -I../hqc/src/common/hqc-1 -I../hqc/src/x86_64/avx256 -I../hqc/src/x86_64/avx256/hqc-1 \
		-I../hqc/lib/fips202 -Ibuild-hqc-avx2/src -Irandombytes/ \
		build-hqc-avx2/src/CMakeFiles/hqc_1_x86_64.dir/common/*.c.o \
		build-hqc-avx2/src/CMakeFiles/hqc_1_x86_64.dir/x86_64/avx256/*.c.o \
		build-hqc-avx2/src/CMakeFiles/hqc_1_x86_64.dir/x86_64/avx256/hqc-1/*.c.o \
		build-hqc-avx2/lib/CMakeFiles/fips202.dir/*.c.o \
		randombytes/librandombytes1.a

bin/benchmark-hqc-3-ref: build-hqc-ref randombytes/librandombytes1.a
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-I../hqc/src/common -I../hqc/src/common/hqc-3 -I../hqc/src/ref -I../hqc/src/ref/hqc-3 \
		-I../hqc/lib/fips202 -Ibuild-hqc-ref/src -Irandombytes/ \
		build-hqc-ref/src/CMakeFiles/hqc_3_ref.dir/common/*.c.o \
		build-hqc-ref/src/CMakeFiles/hqc_3_ref.dir/ref/*.c.o \
		build-hqc-ref/src/CMakeFiles/hqc_3_ref.dir/ref/hqc-3/*.c.o \
		build-hqc-ref/lib/CMakeFiles/fips202.dir/*.c.o \
		randombytes/librandombytes1.a

bin/benchmark-hqc-3-avx2: build-hqc-avx2 randombytes/librandombytes1.a
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-I../hqc/src/common -I../hqc/src/common/hqc-3 -I../hqc/src/x86_64/avx256 -I../hqc/src/x86_64/avx256/hqc-3 \
		-I../hqc/lib/fips202 -Ibuild-hqc-avx2/src -Irandombytes/ \
		build-hqc-avx2/src/CMakeFiles/hqc_3_x86_64.dir/common/*.c.o \
		build-hqc-avx2/src/CMakeFiles/hqc_3_x86_64.dir/x86_64/avx256/*.c.o \
		build-hqc-avx2/src/CMakeFiles/hqc_3_x86_64.dir/x86_64/avx256/hqc-3/*.c.o \
		build-hqc-avx2/lib/CMakeFiles/fips202.dir/*.c.o \
		randombytes/librandombytes1.a

bin/benchmark-hqc-5-ref: build-hqc-ref randombytes/librandombytes1.a
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-I../hqc/src/common -I../hqc/src/common/hqc-5 -I../hqc/src/ref -I../hqc/src/ref/hqc-5 \
		-I../hqc/lib/fips202 -Ibuild-hqc-ref/src -Irandombytes/ \
		build-hqc-ref/src/CMakeFiles/hqc_5_ref.dir/common/*.c.o \
		build-hqc-ref/src/CMakeFiles/hqc_5_ref.dir/ref/*.c.o \
		build-hqc-ref/src/CMakeFiles/hqc_5_ref.dir/ref/hqc-5/*.c.o \
		build-hqc-ref/lib/CMakeFiles/fips202.dir/*.c.o \
		randombytes/librandombytes1.a

bin/benchmark-hqc-5-avx2: build-hqc-avx2 randombytes/librandombytes1.a
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-I../hqc/src/common -I../hqc/src/common/hqc-5 -I../hqc/src/x86_64/avx256 -I../hqc/src/x86_64/avx256/hqc-5 \
		-I../hqc/lib/fips202 -Ibuild-hqc-avx2/src -Irandombytes/ \
		build-hqc-avx2/src/CMakeFiles/hqc_5_x86_64.dir/common/*.c.o \
		build-hqc-avx2/src/CMakeFiles/hqc_5_x86_64.dir/x86_64/avx256/*.c.o \
		build-hqc-avx2/src/CMakeFiles/hqc_5_x86_64.dir/x86_64/avx256/hqc-5/*.c.o \
		build-hqc-avx2/lib/CMakeFiles/fips202.dir/*.c.o \
		randombytes/librandombytes1.a

#-- Combined PQC benchmarks ------------------------------------------

compile-pqc: compile-frodokem compile-hqc
run-pqc: run-frodokem run-hqc

#-- kaiburr-jasmin benchmarks ----------------------------------------

../kaiburr-jasmin/code/jasmin/kaiburr4/avx2/jkem.s:
	$(MAKE) -C ../kaiburr-jasmin/code/jasmin/kaiburr4/avx2/ jkem.s

../kaiburr-jasmin/code/jasmin/kaiburr6/avx2/jkem.s:
	$(MAKE) -C ../kaiburr-jasmin/code/jasmin/kaiburr6/avx2/ jkem.s

../kaiburr-jasmin/code/jasmin/kaiburr8/avx2/jkem.s:
	$(MAKE) -C ../kaiburr-jasmin/code/jasmin/kaiburr8/avx2/ jkem.s

bin/kaiburr4-jasmin-avx2: randombytes/librandombytes1.a ../kaiburr-jasmin/code/jasmin/kaiburr4/avx2/jkem.s
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-DJADE_NAMESPACE=JADE_KEM_mlkem_kaiburr4_amd64_avx2 \
		-DJADE_NAMESPACE_LC=jade_kem_mlkem_kaiburr4_amd64_avx2 \
		-Irandombytes/ \
		-I../kaiburr-jasmin/code/jasmin/kaiburr4/avx2/include/ \
		../kaiburr-jasmin/code/jasmin/kaiburr4/avx2/jkem.s \
		randombytes/librandombytes1.a

bin/kaiburr6-jasmin-avx2: randombytes/librandombytes1.a ../kaiburr-jasmin/code/jasmin/kaiburr6/avx2/jkem.s
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-DJADE_NAMESPACE=JADE_KEM_mlkem_kaiburr6_amd64_avx2 \
		-DJADE_NAMESPACE_LC=jade_kem_mlkem_kaiburr6_amd64_avx2 \
		-Irandombytes/ \
		-I../kaiburr-jasmin/code/jasmin/kaiburr6/avx2/include/ \
		../kaiburr-jasmin/code/jasmin/kaiburr6/avx2/jkem.s \
		randombytes/librandombytes1.a

bin/kaiburr8-jasmin-avx2: randombytes/librandombytes1.a ../kaiburr-jasmin/code/jasmin/kaiburr8/avx2/jkem.s
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-DJADE_NAMESPACE=JADE_KEM_mlkem_kaiburr8_amd64_avx2 \
		-DJADE_NAMESPACE_LC=jade_kem_mlkem_kaiburr8_amd64_avx2 \
		-Irandombytes/ \
		-I../kaiburr-jasmin/code/jasmin/kaiburr8/avx2/include/ \
		../kaiburr-jasmin/code/jasmin/kaiburr8/avx2/jkem.s \
		randombytes/librandombytes1.a

#-- kaiburr-c benchmarks -----------------------------------------------

bin/kaiburr-c-ref: randombytes/librandombytes1.a
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-DJADE_NAMESPACE=KAIBURR_C_ref \
		-DJADE_NAMESPACE_LC=kaiburr_c_ref \
		-Irandombytes/ \
		-I../kaiburr-c/ref/ \
		../kaiburr-c/ref/kem.c ../kaiburr-c/ref/indcpa.c ../kaiburr-c/ref/poly.c \
		../kaiburr-c/ref/polyvec.c ../kaiburr-c/ref/reduce.c ../kaiburr-c/ref/ntt.c \
		../kaiburr-c/ref/verify.c ../kaiburr-c/ref/fips202.c ../kaiburr-c/ref/fn.c \
		randombytes/librandombytes1.a

bin/kaiburr-c-avx2: randombytes/librandombytes1.a
	$(CC) $(CFLAGS) -o $@ src/crypto_kem.c \
		-DJADE_NAMESPACE=KAIBURR_C_avx2 \
		-DJADE_NAMESPACE_LC=kaiburr_c_avx2 \
		-Irandombytes/ \
		-I../kaiburr-c/avx2/ \
		../kaiburr-c/avx2/kem.c ../kaiburr-c/avx2/indcpa.c ../kaiburr-c/avx2/poly.c \
		../kaiburr-c/avx2/polyvec.c ../kaiburr-c/avx2/fips202x4.c ../kaiburr-c/avx2/fn.c \
		../kaiburr-c/avx2/verify.c ../kaiburr-c/avx2/consts.c ../kaiburr-c/avx2/rejsample.c \
		randombytes/librandombytes1.a

#-- randombytes --------------------------------------------------------

randombytes/librandombytes1.a:
	$(MAKE) -C randombytes/

#-- misc ----------------------------------------------------------------

.PHONY: clean
clean:
	$(RM) -f bin/*
	$(RM) -rf build-hqc-ref build-hqc-avx2
	$(MAKE) -C randombytes/ clean

.PHONY: help
help:
	@echo "Unified benchmark harness for all KEM implementations"
	@echo ""
	@echo "Kaiburr targets:"
	@echo "  make compile       - Build Jasmin implementations (default)"
	@echo "  make compile-c     - Build C implementations"
	@echo "  make compile-all   - Build all Kaiburr implementations"
	@echo "  make run-jasmin    - Run Jasmin benchmarks (default)"
	@echo "  make run-c         - Run C benchmarks"
	@echo "  make run           - Run all Kaiburr benchmarks"
	@echo ""
	@echo "FrodoKEM targets:"
	@echo "  make compile-frodokem-ref   - Build FrodoKEM reference (640, 976, 1344)"
	@echo "  make compile-frodokem-avx2  - Build FrodoKEM AVX2 (640, 976, 1344)"
	@echo "  make compile-frodokem       - Build all FrodoKEM variants"
	@echo "  make run-frodokem-ref       - Run FrodoKEM reference benchmarks"
	@echo "  make run-frodokem-avx2      - Run FrodoKEM AVX2 benchmarks"
	@echo "  make run-frodokem           - Run all FrodoKEM benchmarks"
	@echo ""
	@echo "HQC targets:"
	@echo "  make compile-hqc-ref        - Build HQC reference (1, 3, 5)"
	@echo "  make compile-hqc-avx2       - Build HQC AVX2 (1, 3, 5)"
	@echo "  make compile-hqc            - Build all HQC variants"
	@echo "  make run-hqc-ref            - Run HQC reference benchmarks"
	@echo "  make run-hqc-avx2           - Run HQC AVX2 benchmarks"
	@echo "  make run-hqc                - Run all HQC benchmarks"
	@echo ""
	@echo "Combined PQC targets:"
	@echo "  make compile-pqc            - Build all FrodoKEM and HQC variants"
	@echo "  make run-pqc                - Run all FrodoKEM and HQC benchmarks"
	@echo ""
	@echo "Utility targets:"
	@echo "  make clean                  - Clean all build artifacts"
	@echo "  make help                   - Show this help message"
	@echo ""
	@echo "Variables:"
	@echo "  CPU                - CPU identifier for output (default: empty)"
	@echo "  CFLAGS             - Compiler flags (default: -Wall -O3 ...)"
	@echo ""
	@echo "Examples:"
	@echo "  make run CPU=Ryzen5                 # Run all Kaiburr benchmarks"
	@echo "  make run-pqc CPU=Ryzen5             # Run all PQC benchmarks"
	@echo "  make compile-frodokem && make run-frodokem-ref   # Build and run FrodoKEM ref"
