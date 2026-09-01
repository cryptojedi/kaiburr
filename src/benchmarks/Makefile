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
	$(MAKE) -C randombytes/ clean

.PHONY: help
help:
	@echo "Unified benchmark harness for Kaiburr KEM implementations"
	@echo ""
	@echo "Targets:"
	@echo "  make compile       - Build Jasmin implementations (default)"
	@echo "  make compile-c     - Build C implementations"
	@echo "  make compile-all   - Build all Kaiburr implementations"
	@echo "  make run-jasmin    - Run Jasmin benchmarks (default)"
	@echo "  make run-c         - Run C benchmarks"
	@echo "  make run           - Run all Kaiburr benchmarks"
	@echo ""
	@echo "Utility targets:"
	@echo "  make clean         - Clean all build artifacts"
	@echo "  make help          - Show this help message"
	@echo ""
	@echo "Variables:"
	@echo "  CPU                - CPU identifier for output (default: empty)"
	@echo "  CFLAGS             - Compiler flags (default: -Wall -O3 ...)"
	@echo ""
	@echo "Examples:"
	@echo "  make run CPU=Ryzen5          # Run all Kaiburr benchmarks"
	@echo "  make compile-all && make run # Build and run all implementations"
