#include "api.h"
#include "randombytes1.h"

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <inttypes.h>

//
// Handle both namespace-based (kaiburr) and direct API (frodokem, hqc) KEMs
//

#ifdef NAMESPACE
// Kaiburr-style namespace system
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
// (already #define'd by api.h from frodokem/hqc)
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

void print_results_op5(
  const char *cpu,
  const char *impl,
  int print_header,
  uint64_t med[5][RUNS],
  uint64_t q1[5][RUNS],
  uint64_t q3[5][RUNS]
){
  #ifdef RUNS_SORT
  for(size_t i=0; i<5; i++)
  { qsort(&(med[i][0]), RUNS, sizeof(uint64_t), cmp_uint64); }
  #endif

  if(print_header)
  { printf("|        cpu |              implem. |           keypair |      keypair_derand ");
    printf("|             enc |        enc_derand |             dec |\n");
    printf("|-----------:|---------------------:|-------------------:|--------------------:");
    printf("|-------------------:|-------------------:|-------------------:|\n");
  }

  printf("|%12.11s", cpu);
  printf("|%22.21s", impl);

  printf("|%" PRIu64 " (%" PRIu64 " - %" PRIu64 ")", med[0][RUNS/2], q1[0][RUNS/2], q3[0][RUNS/2]);
  printf("|%" PRIu64 " (%" PRIu64 " - %" PRIu64 ")", med[1][RUNS/2], q1[1][RUNS/2], q3[1][RUNS/2]);
  printf("|%" PRIu64 " (%" PRIu64 " - %" PRIu64 ")", med[2][RUNS/2], q1[2][RUNS/2], q3[2][RUNS/2]);
  printf("|%" PRIu64 " (%" PRIu64 " - %" PRIu64 ")", med[3][RUNS/2], q1[3][RUNS/2], q3[3][RUNS/2]);
  printf("|%" PRIu64 " (%" PRIu64 " - %" PRIu64 ")", med[4][RUNS/2], q1[4][RUNS/2], q3[4][RUNS/2]);
  printf("|\n");
}

void print_results_op3(
  const char *cpu,
  const char *impl,
  int print_header,
  uint64_t med[3][RUNS],
  uint64_t q1[3][RUNS],
  uint64_t q3[3][RUNS]
){
  #ifdef RUNS_SORT
  for(size_t i=0; i<3; i++)
  { qsort(&(med[i][0]), RUNS, sizeof(uint64_t), cmp_uint64); }
  #endif

  if(print_header)
  { printf("|        cpu |              implem. |           keypair |             enc |             dec |\n");
    printf("|-----------:|---------------------:|-------------------:|-------------------:|-------------------:|\n");
  }

  printf("|%12.11s", cpu);
  printf("|%22.21s", impl);

  printf("|%" PRIu64 " (%" PRIu64 " - %" PRIu64 ")", med[0][RUNS/2], q1[0][RUNS/2], q3[0][RUNS/2]);
  printf("|%" PRIu64 " (%" PRIu64 " - %" PRIu64 ")", med[1][RUNS/2], q1[1][RUNS/2], q3[1][RUNS/2]);
  printf("|%" PRIu64 " (%" PRIu64 " - %" PRIu64 ")", med[2][RUNS/2], q1[2][RUNS/2], q3[2][RUNS/2]);
  printf("|\n");
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

  // 'derand' (optional)
  uint8_t *_d_ss,  *d_ss,  *d_s;  // CRYPTO_SECRETKEYBYTES    // keypair, dec
  uint8_t *_d_ps,  *d_ps,  *d_p;  // CRYPTO_PUBLICKEYBYTES    // keypair, enc
  uint8_t *_d_cs,  *d_cs,  *d_c;  // CRYPTO_CIPHERTEXTBYTES   // enc, dec
  uint8_t *_d_ks,  *d_ks,  *d_k;  // CRYPTO_BYTES             // enc
  uint8_t *_d_kcs, *d_kcs, *d_kc; // CRYPTO_KEYPAIRCOINBYTES  // keypair
  uint8_t *_d_ecs, *d_ecs, *d_ec; // CRYPTO_ENCCOINBYTES      // enc

  size_t slen, plen, clen, klen, tlen;
  size_t kclen, eclen;

  slen  = alignedcalloc_step(CRYPTO_SECRETKEYBYTES);
  plen  = alignedcalloc_step(CRYPTO_PUBLICKEYBYTES);
  clen  = alignedcalloc_step(CRYPTO_CIPHERTEXTBYTES);
  klen  = alignedcalloc_step(CRYPTO_BYTES);
  tlen  = alignedcalloc_step(CRYPTO_BYTES);

  #if HAS_KEYPAIR_DERAND
  kclen = alignedcalloc_step(CRYPTO_KEYPAIRCOINBYTES);
  #else
  kclen = 0;
  #endif

  #if HAS_ENC_DERAND
  eclen = alignedcalloc_step(CRYPTO_ENCCOINBYTES);
  #else
  eclen = 0;
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

  #if OP == 5
  print_results_op5(cpu_name, implementation_name, print_headers, (uint64_t(*)[RUNS])median, (uint64_t(*)[RUNS])q1, (uint64_t(*)[RUNS])q3);
  #else
  print_results_op3(cpu_name, implementation_name, print_headers, (uint64_t(*)[RUNS])median, (uint64_t(*)[RUNS])q1, (uint64_t(*)[RUNS])q3);
  #endif

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

