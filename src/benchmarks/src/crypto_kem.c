#ifndef KEM_API_HEADER
#define KEM_API_HEADER "api.h"
#endif
#include KEM_API_HEADER

#include "randombytes1.h"

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <inttypes.h>

#ifdef JADE_NAMESPACE
// kaiburr-style namespace system
#include "namespace.h"
#define CRYPTO_SECRETKEYBYTES     NAMESPACE(SECRETKEYBYTES)
#define CRYPTO_PUBLICKEYBYTES     NAMESPACE(PUBLICKEYBYTES)
#define CRYPTO_KEYPAIRCOINBYTES   NAMESPACE(KEYPAIRCOINBYTES)
#define CRYPTO_CIPHERTEXTBYTES    NAMESPACE(CIPHERTEXTBYTES)
#define CRYPTO_BYTES              NAMESPACE(BYTES)
#define CRYPTO_ENCCOINBYTES       NAMESPACE(ENCCOINBYTES)
#define CRYPTO_ALGNAME            NAMESPACE(ALGNAME)
#define CRYPTO_ARCH               NAMESPACE(ARCH)
#define CRYPTO_IMPL               NAMESPACE(IMPL)
#define crypto_kem_keypair        NAMESPACE_LC(keypair)
#define crypto_kem_keypair_derand NAMESPACE_LC(keypair_derand)
#define crypto_kem_enc            NAMESPACE_LC(enc)
#define crypto_kem_enc_derand     NAMESPACE_LC(enc_derand)
#define crypto_kem_dec            NAMESPACE_LC(dec)
#else
// Direct API - use api.h defines directly
#endif

// Determine which operations are available
#ifdef crypto_kem_keypair_derand
#define HAS_KEYPAIR_DERAND 1
#else
#define HAS_KEYPAIR_DERAND 0
#endif

#ifdef crypto_kem_enc_derand
#define HAS_ENC_DERAND 1
#else
#define HAS_ENC_DERAND 0
#endif

#if HAS_KEYPAIR_DERAND && HAS_ENC_DERAND
#define OP 5
#else
#define OP 3
#endif

//

#include "config.h"
#include "cpucycles.c"
#include "alignedcalloc.c"

//
//
// HQC's crypto_kem_keypair()/crypto_kem_enc() draw from a SHAKE-256 PRNG that
// the caller is required to seed first. Without this the benchmark would run off an all-zero
// state. We seed it from the same getrandom()-backed randombytes() that
// FrodoKEM and Kaiburr use, so all three draw their entropy from one source.
//
// prng_init is declared here rather than pulled in via HQC's symmetric.h so
// that this driver does not need HQC's parameters.h/data_structures.h on the
// include path.
//

#ifdef BENCH_HQC_PRNG_INIT
void prng_init(uint8_t *entropy_input, uint8_t *personalization_string,
               uint32_t enlen, uint32_t perlen);

static void bench_init(void)
{
  uint8_t entropy[48];
  uint8_t personalization[1] = {0};
  randombytes(entropy, sizeof entropy);
  prng_init(entropy, personalization, (uint32_t)sizeof entropy, 0);
}
#else
static void bench_init(void) {}
#endif

//

#define CELL_W 28

static void print_head_cell(const char *name)
{ printf("|%*s", CELL_W, name); }

static void print_rule_cell(void)
{ for(int i=0; i<CELL_W-1; i++) putchar('-'); printf(":"); putchar('|'); }

static void print_cell(uint64_t med, uint64_t q1, uint64_t q3)
{
  char buf[64];
  snprintf(buf, sizeof buf,
           "%" PRIu64 " (%" PRIu64 "-%" PRIu64 ")", med, q1, q3);
  printf("|%*s", CELL_W, buf);
}

#if RUNS_SORT
static void sort_runs(uint64_t *med, uint64_t *q1, uint64_t *q3, size_t n)
{
  size_t i, j;
  for(i = 1; i < n; i++)
  { uint64_t m = med[i], a = q1[i], b = q3[i];
    for(j = i; j > 0 && med[j-1] > m; j--)
    { med[j] = med[j-1]; q1[j] = q1[j-1]; q3[j] = q3[j-1]; }
    med[j] = m; q1[j] = a; q3[j] = b;
  }
}
#endif

#define COLS 5

static void print_results(
  const char *cpu,
  const char *impl,
  int print_header,
  size_t ops,
  uint64_t med[][RUNS],
  uint64_t q1[][RUNS],
  uint64_t q3[][RUNS]
){
  static const char *names[COLS] =
    { "keypair", "keypair_derand", "enc", "enc_derand", "dec" };

  static const int slot5[5] = { 0, 1, 2, 3, 4 };
  static const int slot3[3] = { 0, 2, 4 };
  const int *slot = (ops == COLS) ? slot5 : slot3;

  int filled[COLS] = {0};
  size_t i;

  #if RUNS_SORT
  for(i=0; i<ops; i++)
  { sort_runs(&(med[i][0]), &(q1[i][0]), &(q3[i][0]), RUNS); }
  #endif

  if(print_header)
  { printf("|%12s|%22s", "cpu", "implem.");
    for(i=0; i<COLS; i++){ print_head_cell(names[i]); }
    printf("|\n");
    printf("|-----------:|---------------------:|");
    for(i=0; i<COLS; i++){ print_rule_cell(); }
    printf("\n");
  }

  printf("|%12.11s", cpu);
  printf("|%22.21s", impl);
  for(i=0; i<ops; i++){ filled[slot[i]] = 1; }
  for(i=0; i<COLS; i++)
  { if(filled[i])
    { size_t src = (ops == COLS) ? i : (i / 2);
      print_cell(med[src][RUNS/2], q1[src][RUNS/2], q3[src][RUNS/2]);
    }
    else
    { printf("|%*s", CELL_W, "n/a"); }
  }
  printf("|\n");
  fflush(stdout);
}

//

int main(int argc, char**argv)
{
  const char *cpu_name = "";
  const char *implementation_name = "";
  int print_headers = 1;

  if (argc > 1) cpu_name = argv[1];
  if (argc > 2) implementation_name = argv[2];
  if (argc > 3) print_headers = (int)strtol(argv[3], NULL, 10);

  cpucycles_warn_if_not_cycles();
  bench_init();

  size_t run, i;
  uint64_t cycles[TIMINGS];
  uint64_t begin, end;
  uint64_t median[5][RUNS];
  uint64_t q1[5][RUNS];
  uint64_t q3[5][RUNS];
  int r;

  // 'rand'
  uint8_t *_ss,  *ss,  *s;  // CRYPTO_SECRETKEYBYTES  // keypair, dec
  uint8_t *_ps,  *ps,  *p;  // CRYPTO_PUBLICKEYBYTES  // keypair, enc
  uint8_t *_cs,  *cs,  *c;  // CRYPTO_CIPHERTEXTBYTES // enc, dec
  uint8_t *_ks,  *ks,  *k;  // CRYPTO_BYTES           // enc
  uint8_t *_ts,  *ts,  *t;  // CRYPTO_BYTES           // dec

  // 'derand' (only for KEMs that expose the derandomized API)
  #if HAS_KEYPAIR_DERAND || HAS_ENC_DERAND
  uint8_t *_d_ss,  *d_ss,  *d_s;  // CRYPTO_SECRETKEYBYTES    // keypair, dec
  uint8_t *_d_ps,  *d_ps,  *d_p;  // CRYPTO_PUBLICKEYBYTES    // keypair, enc
  uint8_t *_d_cs,  *d_cs,  *d_c;  // CRYPTO_CIPHERTEXTBYTES   // enc, dec
  uint8_t *_d_ks,  *d_ks,  *d_k;  // CRYPTO_BYTES             // enc
  #endif
  #if HAS_KEYPAIR_DERAND
  uint8_t *_d_kcs, *d_kcs, *d_kc; // CRYPTO_KEYPAIRCOINBYTES  // keypair
  size_t kclen;
  #endif
  #if HAS_ENC_DERAND
  uint8_t *_d_ecs, *d_ecs, *d_ec; // CRYPTO_ENCCOINBYTES      // enc
  size_t eclen;
  #endif

  size_t slen, plen, clen, klen, tlen;

  slen  = alignedcalloc_step(CRYPTO_SECRETKEYBYTES);
  plen  = alignedcalloc_step(CRYPTO_PUBLICKEYBYTES);
  clen  = alignedcalloc_step(CRYPTO_CIPHERTEXTBYTES);
  klen  = alignedcalloc_step(CRYPTO_BYTES);
  tlen  = alignedcalloc_step(CRYPTO_BYTES);

  #if HAS_KEYPAIR_DERAND
  kclen = alignedcalloc_step(CRYPTO_KEYPAIRCOINBYTES);
  #endif

  #if HAS_ENC_DERAND
  eclen = alignedcalloc_step(CRYPTO_ENCCOINBYTES);
  #endif

  //

  ss  = alignedcalloc(&_ss,  slen  * TIMINGS);
  ps  = alignedcalloc(&_ps,  plen  * TIMINGS);
  cs  = alignedcalloc(&_cs,  clen  * TIMINGS);
  ks  = alignedcalloc(&_ks,  klen  * TIMINGS);
  ts  = alignedcalloc(&_ts,  tlen  * TIMINGS);

  #if HAS_KEYPAIR_DERAND || HAS_ENC_DERAND
  d_ss  = alignedcalloc(&_d_ss,  slen  * TIMINGS);
  d_ps  = alignedcalloc(&_d_ps,  plen  * TIMINGS);
  d_cs  = alignedcalloc(&_d_cs,  clen  * TIMINGS);
  d_ks  = alignedcalloc(&_d_ks,  klen  * TIMINGS);
  #if HAS_KEYPAIR_DERAND
  d_kcs = alignedcalloc(&_d_kcs, kclen * TIMINGS);
  #endif
  #if HAS_ENC_DERAND
  d_ecs = alignedcalloc(&_d_ecs, eclen * TIMINGS);
  #endif
  #endif

  for (i = 0; i < WARMUP; i++)
  { crypto_kem_keypair(ps, ss);
    crypto_kem_enc(cs, ks, ps);
    crypto_kem_dec(ts, cs, ss);
  }

  for(run = 0; run < RUNS; run++)
  {
    // //////////////////////////////////////////////////
    // keypair
    p = ps; s = ss;
    for (i = 0; i < TIMINGS; i++, p += plen, s += slen)
    { begin = cpucycles_begin();
      r = crypto_kem_keypair(p, s);
      end = cpucycles_end();
      cycles[i] = end - begin;
      assert(r == 0);
    }
    median[0][run] = cpucycles_median(cycles, TIMINGS);
    q1[0][run] = cpucycles_q1(cycles, TIMINGS);
    q3[0][run] = cpucycles_q3(cycles, TIMINGS);

    #if HAS_KEYPAIR_DERAND
    // //////////////////////////////////////////////////
    // keypair derand:
    d_kc = d_kcs;
    for (i = 0; i < TIMINGS; i++, d_kc += kclen)
    { randombytes(d_kc, CRYPTO_KEYPAIRCOINBYTES); }

    d_p = d_ps; d_s = d_ss; d_kc = d_kcs;
    for (i = 0; i < TIMINGS; i++, d_p += plen, d_s += slen, d_kc += kclen)
    { begin = cpucycles_begin();
      r = crypto_kem_keypair_derand(d_p, d_s, d_kc);
      end = cpucycles_end();
      cycles[i] = end - begin;
      assert(r == 0);
    }
    median[1][run] = cpucycles_median(cycles, TIMINGS);
    q1[1][run] = cpucycles_q1(cycles, TIMINGS);
    q3[1][run] = cpucycles_q3(cycles, TIMINGS);
    #endif

    // //////////////////////////////////////////////////
    // enc
    c = cs; k = ks; p = ps;
    for (i = 0; i < TIMINGS; i++, c += clen, k += klen, p += plen)
    { begin = cpucycles_begin();
      r = crypto_kem_enc(c, k, p);
      end = cpucycles_end();
      cycles[i] = end - begin;
      assert(r == 0);
    }
    #if HAS_KEYPAIR_DERAND
    median[2][run] = cpucycles_median(cycles, TIMINGS);
    q1[2][run] = cpucycles_q1(cycles, TIMINGS);
    q3[2][run] = cpucycles_q3(cycles, TIMINGS);
    #else
    median[1][run] = cpucycles_median(cycles, TIMINGS);
    q1[1][run] = cpucycles_q1(cycles, TIMINGS);
    q3[1][run] = cpucycles_q3(cycles, TIMINGS);
    #endif

    #if HAS_ENC_DERAND
    // //////////////////////////////////////////////////
    // enc derand
    d_ec = d_ecs;
    for (i = 0; i < TIMINGS; i++, d_ec += eclen)
    { randombytes(d_ec, CRYPTO_ENCCOINBYTES); }

    d_c = d_cs; d_k = d_ks; d_p = d_ps; d_ec = d_ecs;
    for (i = 0; i < TIMINGS; i++, d_c += clen, d_k += klen, d_p += plen, d_ec += eclen)
    { begin = cpucycles_begin();
      r = crypto_kem_enc_derand(d_c, d_k, d_p, d_ec);
      end = cpucycles_end();
      cycles[i] = end - begin;
      assert(r == 0);
    }
    #if HAS_KEYPAIR_DERAND
    median[3][run] = cpucycles_median(cycles, TIMINGS);
    q1[3][run] = cpucycles_q1(cycles, TIMINGS);
    q3[3][run] = cpucycles_q3(cycles, TIMINGS);
    #else
    median[2][run] = cpucycles_median(cycles, TIMINGS);
    q1[2][run] = cpucycles_q1(cycles, TIMINGS);
    q3[2][run] = cpucycles_q3(cycles, TIMINGS);
    #endif
    #endif

    // //////////////////////////////////////////////////
    // dec
    t = ts; c = cs; s = ss;
    for (i = 0; i < TIMINGS; i++, t += tlen, c += clen, s += slen)
    { begin = cpucycles_begin();
      r = crypto_kem_dec(t, c, s);
      end = cpucycles_end();
      cycles[i] = end - begin;
      assert(r == 0);
    }
    #if HAS_KEYPAIR_DERAND
    #if HAS_ENC_DERAND
    median[4][run] = cpucycles_median(cycles, TIMINGS);
    q1[4][run] = cpucycles_q1(cycles, TIMINGS);
    q3[4][run] = cpucycles_q3(cycles, TIMINGS);
    #else
    median[3][run] = cpucycles_median(cycles, TIMINGS);
    q1[3][run] = cpucycles_q1(cycles, TIMINGS);
    q3[3][run] = cpucycles_q3(cycles, TIMINGS);
    #endif
    #else
    median[2][run] = cpucycles_median(cycles, TIMINGS);
    q1[2][run] = cpucycles_q1(cycles, TIMINGS);
    q3[2][run] = cpucycles_q3(cycles, TIMINGS);
    #endif

    // //////////////////////////////////////////////////
    // check that shared_secrets match
    k = ks; t = ts;
    for (i = 0; i < TIMINGS; i++, k += klen, t += tlen)
    { assert(memcmp(k, t, CRYPTO_BYTES) == 0); }

    #if HAS_KEYPAIR_DERAND || HAS_ENC_DERAND
    d_k = d_ks; t = ts; d_c = d_cs; d_s = d_ss;
    for (i = 0; i < TIMINGS; i++, d_k += klen, t += tlen, d_c += clen, d_s += slen)
    { crypto_kem_dec(t, d_c, d_s);
      assert(memcmp(d_k, t, CRYPTO_BYTES) == 0);
    }
    #endif
  }

  print_results(cpu_name, implementation_name, print_headers, OP, median, q1, q3);

  free(_ps);
  free(_ss);
  free(_ks);
  free(_cs);
  free(_ts);

  #if HAS_KEYPAIR_DERAND || HAS_ENC_DERAND
  free(_d_ps);
  free(_d_ss);
  free(_d_ks);
  free(_d_cs);
  #if HAS_KEYPAIR_DERAND
  free(_d_kcs);
  #endif
  #if HAS_ENC_DERAND
  free(_d_ecs);
  #endif
  #endif

  return 0;
}

