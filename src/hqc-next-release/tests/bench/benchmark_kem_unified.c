#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>

#include "api.h"
#include "config.h"
#include "cpucycles.c"
#include "alignedcalloc.c"

#define OPS 3

static int cmp_uint64(const void *a, const void *b)
{
  if(*(uint64_t *)a < *(uint64_t *)b){ return -1; }
  if(*(uint64_t *)a > *(uint64_t *)b){ return 1; }
  return 0;
}

void print_results(int print_header, uint64_t med[OPS][RUNS], uint64_t q1[OPS][RUNS], uint64_t q3[OPS][RUNS])
{
  const char *op_names[OPS] = {"keypair", "encaps", "decaps"};

  #ifdef RUNS_SORT
  for(size_t i = 0; i < OPS; i++) {
    qsort(&(med[i][0]), RUNS, sizeof(uint64_t), cmp_uint64);
  }
  #endif

  if(print_header) {
    printf("|           operation |");
    for(size_t i = 0; i < RUNS; i++) {
      printf("        run %zu |", i);
    }
    printf("\n");
    printf("|--------------------:|");
    for(size_t i = 0; i < RUNS; i++) {
      printf("-----------------:|");
    }
    printf("\n");
  }

  for(size_t op = 0; op < OPS; op++) {
    printf("| %18s |", op_names[op]);
    for(size_t run = 0; run < RUNS; run++) {
      printf(" %15" PRIu64 " |", med[op][run]);
    }
    printf("\n");
  }
}

int main(void)
{
  uint8_t *pk, *sk, *ct, *ss1, *ss2;
  uint8_t *pk_free, *sk_free, *ct_free, *ss1_free, *ss2_free;

  pk = alignedcalloc(&pk_free, PUBLIC_KEY_BYTES);
  sk = alignedcalloc(&sk_free, SECRET_KEY_BYTES);
  ct = alignedcalloc(&ct_free, CIPHERTEXT_BYTES);
  ss1 = alignedcalloc(&ss1_free, SHARED_SECRET_BYTES);
  ss2 = alignedcalloc(&ss2_free, SHARED_SECRET_BYTES);

  uint64_t med[OPS][RUNS];
  uint64_t q1[OPS][RUNS];
  uint64_t q3[OPS][RUNS];

  for(size_t run = 0; run < RUNS; run++) {
    uint64_t cycles[TIMINGS];

    for(size_t i = 0; i < TIMINGS; i++) {
      uint64_t t0 = cpucycles_begin();
      crypto_kem_keypair(pk, sk);
      uint64_t t1 = cpucycles_end();
      cycles[i] = t1 - t0;
    }
    qsort(cycles, TIMINGS, sizeof(uint64_t), cmp_uint64);
    med[0][run] = cpucycles_median(cycles, TIMINGS);
    q1[0][run] = cpucycles_q1(cycles, TIMINGS);
    q3[0][run] = cpucycles_q3(cycles, TIMINGS);

    for(size_t i = 0; i < TIMINGS; i++) {
      uint64_t t0 = cpucycles_begin();
      crypto_kem_enc(ct, ss1, pk);
      uint64_t t1 = cpucycles_end();
      cycles[i] = t1 - t0;
    }
    qsort(cycles, TIMINGS, sizeof(uint64_t), cmp_uint64);
    med[1][run] = cpucycles_median(cycles, TIMINGS);
    q1[1][run] = cpucycles_q1(cycles, TIMINGS);
    q3[1][run] = cpucycles_q3(cycles, TIMINGS);

    for(size_t i = 0; i < TIMINGS; i++) {
      uint64_t t0 = cpucycles_begin();
      crypto_kem_dec(ss2, ct, sk);
      uint64_t t1 = cpucycles_end();
      cycles[i] = t1 - t0;
    }
    qsort(cycles, TIMINGS, sizeof(uint64_t), cmp_uint64);
    med[2][run] = cpucycles_median(cycles, TIMINGS);
    q1[2][run] = cpucycles_q1(cycles, TIMINGS);
    q3[2][run] = cpucycles_q3(cycles, TIMINGS);
  }

  print_results(1, med, q1, q3);

  free(pk_free);
  free(sk_free);
  free(ct_free);
  free(ss1_free);
  free(ss2_free);

  return 0;
}
