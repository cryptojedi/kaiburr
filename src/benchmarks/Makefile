# unified KEM benchmark harness
#
#   make help      list targets
#   make run       every implementation, one table
#   make smoke     same, but TIMINGS=101, to check the build

CFLAGS ?= -Wall -O3 -fomit-frame-pointer -march=native

CPU ?= $(shell sed -n 's/^model name[[:space:]]*: *//p' /proc/cpuinfo 2>/dev/null | head -1)

TIMINGS ?= 10001
RUNS    ?= 3
BENCHFLAGS := -DTIMINGS=$(TIMINGS) -DRUNS=$(RUNS)

DRIVER := src/crypto_kem.c
RB     := randombytes/librandombytes1.a
RBINC  := -Irandombytes/

KAIBURR_C      := ../kaiburr-c
KAIBURR_JASMIN := ../kaiburr-jasmin
FRODO          := ../PQCrypto-LWEKE
HQC            := ../hqc-next-release

JASMINC ?= jasminc
KECCAK  := $(KAIBURR_JASMIN)/formosa-keccak/src/amd64

KAIBURR_VARIANTS := kaiburr4:7 kaiburr6:18 kaiburr8:24
HQC_VARIANTS     := hqc-1 hqc-3 hqc-5

KAIBURR_C_BINS      := $(foreach v,$(KAIBURR_VARIANTS),bin/$(firstword $(subst :, ,$(v)))-c-ref bin/$(firstword $(subst :, ,$(v)))-c-avx2)
KAIBURR_JASMIN_BINS := $(foreach v,$(KAIBURR_VARIANTS),bin/$(firstword $(subst :, ,$(v)))-jasmin-ref bin/$(firstword $(subst :, ,$(v)))-jasmin-avx2)
HQC_BINS            := $(foreach v,$(HQC_VARIANTS),bin/$(v)-ref bin/$(v)-avx2)
FRODO_BINS          := bin/frodo640-shake-ref bin/frodo640-shake-avx2

KAIBURR_BINS := $(KAIBURR_C_BINS) $(KAIBURR_JASMIN_BINS)
ALL_BINS     := $(KAIBURR_BINS) $(HQC_BINS) $(FRODO_BINS)

.PHONY: default all run smoke help clean \
        compile compile-kaiburr compile-kaiburr-c compile-kaiburr-jasmin \
        compile-hqc compile-frodo \
        run-kaiburr run-kaiburr-c run-kaiburr-jasmin run-hqc run-frodo

default: run

compile: $(ALL_BINS)
compile-kaiburr:        $(KAIBURR_BINS)
compile-kaiburr-c:      $(KAIBURR_C_BINS)
compile-kaiburr-jasmin: $(KAIBURR_JASMIN_BINS)
compile-hqc:            $(HQC_BINS)
compile-frodo:          $(FRODO_BINS)

define run_group
@set -e; hdr=$(2); for b in $(1); do \
  ./$$b "$(CPU)" "$$(basename $$b)" $$hdr; hdr=0; \
done
endef

run: $(ALL_BINS)
	$(call run_group,$(KAIBURR_JASMIN_BINS),1)
	$(call run_group,$(KAIBURR_C_BINS),0)
	$(call run_group,$(HQC_BINS),0)
	$(call run_group,$(FRODO_BINS),0)

run-kaiburr: $(KAIBURR_BINS)
	$(call run_group,$(KAIBURR_BINS),1)
run-kaiburr-c: $(KAIBURR_C_BINS)
	$(call run_group,$(KAIBURR_C_BINS),1)
run-kaiburr-jasmin: $(KAIBURR_JASMIN_BINS)
	$(call run_group,$(KAIBURR_JASMIN_BINS),1)
run-hqc: $(HQC_BINS)
	$(call run_group,$(HQC_BINS),1)
run-frodo: $(FRODO_BINS)
	$(call run_group,$(FRODO_BINS),1)

smoke:
	@$(MAKE) --no-print-directory TIMINGS=101 RUNS=1 run

KAIBURR_C_REF_SRCS = kem.c indcpa.c polyvec.c poly.c ntt.c fn.c reduce.c \
                     verify.c fips202.c symmetric-shake.c

KAIBURR_C_AVX2_SRCS = kem.c indcpa.c polyvec.c poly.c consts.c rejsample.c \
                      fn.c verify.c fips202.c fips202x4.c symmetric-shake.c \
                      keccak4x/KeccakP-1600-times4-SIMD256.c \
                      fq.S shuffle.S ntt.S invntt.S basemul.S

define kaiburr_c_defs
-DKYBER_K=$(2) \
-DCRYPTO_SECRETKEYBYTES=$(1)_SECRETKEYBYTES \
-DCRYPTO_PUBLICKEYBYTES=$(1)_PUBLICKEYBYTES \
-DCRYPTO_CIPHERTEXTBYTES=$(1)_CIPHERTEXTBYTES \
-DCRYPTO_KEYPAIRCOINBYTES=$(1)_KEYPAIRCOINBYTES \
-DCRYPTO_ENCCOINBYTES=$(1)_ENCCOINBYTES \
-DCRYPTO_BYTES=$(1)_BYTES \
-Dcrypto_kem_keypair=$(1)_$(3)_keypair \
-Dcrypto_kem_keypair_derand=$(1)_$(3)_keypair_derand \
-Dcrypto_kem_enc=$(1)_$(3)_enc \
-Dcrypto_kem_enc_derand=$(1)_$(3)_enc_derand \
-Dcrypto_kem_dec=$(1)_$(3)_dec
endef

define kaiburr_c_rule
bin/$(1)-c-ref: $(RB) | bin
	$$(CC) $$(CFLAGS) $$(BENCHFLAGS) -o $$@ $$(DRIVER) \
	  $$(call kaiburr_c_defs,$(1),$(2),ref) \
	  -I$$(KAIBURR_C)/ref $$(RBINC) \
	  $$(addprefix $$(KAIBURR_C)/ref/,$$(KAIBURR_C_REF_SRCS)) $$(RB)

bin/$(1)-c-avx2: $(RB) | bin
	$$(CC) $$(CFLAGS) $$(BENCHFLAGS) -mavx2 -mbmi2 -mpopcnt -o $$@ $$(DRIVER) \
	  $$(call kaiburr_c_defs,$(1),$(2),avx2) \
	  -I$$(KAIBURR_C)/avx2 $$(RBINC) \
	  $$(addprefix $$(KAIBURR_C)/avx2/,$$(KAIBURR_C_AVX2_SRCS)) $$(RB)
endef

$(foreach v,$(KAIBURR_VARIANTS),\
  $(eval $(call kaiburr_c_rule,$(firstword $(subst :, ,$(v))),$(word 2,$(subst :, ,$(v))))))

JBUILD := build-jasmin
JSRC    = $(KAIBURR_JASMIN)/code/jasmin

define kaiburr_jasmin_rule
$$(JBUILD)/$(1)/$(2)/jkem.s: \
    $$(wildcard $$(JSRC)/$(1)/$(2)/*.jazz $$(JSRC)/$(1)/$(2)/*.jinc \
                $$(JSRC)/common/$(2)/*.jinc)
	@mkdir -p $$(@D)
	cd $$(JSRC)/$(1)/$(2) && \
	  $$(JASMINC) -I Keccak=$$(abspath $$(KECCAK)) -o $$(abspath $$@) jkem.jazz

bin/$(1)-jasmin-$(2): $(RB) $$(JBUILD)/$(1)/$(2)/jkem.s | bin
	$$(CC) $$(CFLAGS) $$(BENCHFLAGS) -o $$@ $$(DRIVER) \
	  -DJADE_NAMESPACE=JADE_KEM_mlkem_$(1)_amd64_$(2) \
	  -DJADE_NAMESPACE_LC=jade_kem_mlkem_$(1)_amd64_$(2) \
	  -I$$(JSRC)/$(1)/$(2)/include $$(RBINC) \
	  $$(JBUILD)/$(1)/$(2)/jkem.s $$(RB)
endef

$(foreach v,$(KAIBURR_VARIANTS),\
  $(foreach i,ref avx2,\
    $(eval $(call kaiburr_jasmin_rule,$(firstword $(subst :, ,$(v))),$(i)))))

HQC_BUILD_REF  := build-hqc-ref
HQC_BUILD_AVX2 := build-hqc-avx2

$(HQC_BUILD_REF)/.stamp:
	cmake -S $(HQC) -B $(HQC_BUILD_REF) -DHQC_ARCH=ref
	cmake --build $(HQC_BUILD_REF) --target $(subst -,_,$(HQC_VARIANTS:%=%_ref)) -j
	@touch $@

$(HQC_BUILD_AVX2)/.stamp:
	cmake -S $(HQC) -B $(HQC_BUILD_AVX2) -DHQC_ARCH=x86_64 -DHQC_X86_IMPL=avx256
	cmake --build $(HQC_BUILD_AVX2) --target $(subst -,_,$(HQC_VARIANTS:%=%_x86_64)) -j
	@touch $@

define hqc_rule
bin/$(1)-ref: $$(HQC_BUILD_REF)/.stamp $(RB) | bin
	$$(CC) $$(CFLAGS) $$(BENCHFLAGS) -DBENCH_HQC_PRNG_INIT -o $$@ $$(DRIVER) \
	  -I$$(HQC)/src/common/$(1) $$(RBINC) \
	  $$(HQC_BUILD_REF)/src/lib$(2)_ref.a \
	  $$(HQC_BUILD_REF)/lib/libfips202.a $(RB)

bin/$(1)-avx2: $$(HQC_BUILD_AVX2)/.stamp $(RB) | bin
	$$(CC) $$(CFLAGS) $$(BENCHFLAGS) -DBENCH_HQC_PRNG_INIT -o $$@ $$(DRIVER) \
	  -I$$(HQC)/src/common/$(1) $$(RBINC) \
	  $$(HQC_BUILD_AVX2)/src/lib$(2)_x86_64.a \
	  $$(HQC_BUILD_AVX2)/lib/libfips202.a $(RB)
endef

$(foreach v,$(HQC_VARIANTS),$(eval $(call hqc_rule,$(v),$(subst -,_,$(v)))))

FRODO_DEFS := -DNIX -D_AMD64_ -D_SHAKE128_FOR_A_ -DNO_OPENSSL \
              -DKEM_API_HEADER='"api_frodo640.h"' \
              -Dcrypto_kem_keypair=crypto_kem_keypair_Frodo640 \
              -Dcrypto_kem_enc=crypto_kem_enc_Frodo640 \
              -Dcrypto_kem_dec=crypto_kem_dec_Frodo640

bin/frodo640-shake-ref: $(RB) | bin
	$(CC) $(CFLAGS) $(BENCHFLAGS) $(FRODO_DEFS) -D_REFERENCE_ -o $@ $(DRIVER) \
	  -I$(FRODO)/FrodoKEM/src $(RBINC) \
	  $(FRODO)/FrodoKEM/src/frodo640.c $(FRODO)/FrodoKEM/src/util.c \
	  $(FRODO)/common/sha3/fips202.c $(RB) -lm

bin/frodo640-shake-avx2: $(RB) | bin
	$(CC) $(CFLAGS) $(BENCHFLAGS) $(FRODO_DEFS) -D_FAST_ -mavx2 -maes -msse2 -o $@ $(DRIVER) \
	  -I$(FRODO)/FrodoKEM/src -I$(FRODO)/common/sha3/keccak4x $(RBINC) \
	  $(FRODO)/FrodoKEM/src/frodo640.c $(FRODO)/FrodoKEM/src/util.c \
	  $(FRODO)/common/sha3/fips202.c $(FRODO)/common/sha3/fips202x4.c \
	  $(FRODO)/common/sha3/keccak4x/KeccakP-1600-times4-SIMD256.c $(RB) -lm

bin:
	@mkdir -p bin

$(RB):
	$(MAKE) -C randombytes/

.DELETE_ON_ERROR:

clean:
	$(RM) -r bin $(JBUILD) $(HQC_BUILD_REF) $(HQC_BUILD_AVX2)
	$(MAKE) -C randombytes/ clean

help:
	@echo "Unified benchmark harness -- FrodoKEM, HQC and Kaiburr on one driver"
	@echo ""
	@echo "  make run                  build and run everything, one table"
	@echo "  make smoke                same with TIMINGS=101 RUNS=1 (build check)"
	@echo "  make run-kaiburr          kaiburr4/6/8, C and Jasmin, ref and avx2"
	@echo "  make run-kaiburr-c        kaiburr4/6/8, C only"
	@echo "  make run-kaiburr-jasmin   kaiburr4/6/8, Jasmin only"
	@echo "  make run-hqc              hqc-1/3/5, ref and avx2"
	@echo "  make run-frodo            FrodoKEM-640 SHAKE, ref and avx2"
	@echo "  make compile[-<group>]    build without running"
	@echo "  make clean"
	@echo ""
	@echo "Variables:"
	@echo "  CPU=<name>    first column of the table (default: /proc/cpuinfo)"
	@echo "  TIMINGS=n     iterations per operation per run (default 10001)"
	@echo "  RUNS=n        runs per operation (default 3)"
	@echo "  WARMUP=n      untimed iterations before measuring (default 1000)"
	@echo "  CC, CFLAGS, JASMINC"
	@echo ""
	@echo "Run pinned:"
	@echo "  taskset -c 2 make run CPU=\"Xeon 6338\""
