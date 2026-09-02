#ifndef CPUCYCLES_C
#define CPUCYCLES_C

#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <time.h>

#if defined(__x86_64__) || defined(_M_X64)
#define cpucycles_begin cpuid_rdtsc
#define cpucycles_end rdtscp_lfence

static inline uint64_t cpuid_rdtsc(void)
{
    uint32_t lo, hi;

    __asm__ volatile (
        "cpuid\n\t"
        "rdtsc"
        : "=r"(lo), "=r"(hi)
        : "a"(0)
        : "rbx", "rcx", "rdx", "memory"
    );

    return ((uint64_t)hi << 32) | lo;
}

static inline uint64_t rdtscp_lfence(void)
{
  uint32_t lo, hi;

  __asm__ volatile (
    "rdtscp\n\t"
    "lfence"
    : "=r"(lo), "=r"(hi)
    :
    : "rcx", "memory"
  );

  return ((uint64_t)hi << 32) | lo;
}
#else
#define cpucycles_begin monotonic_begin
#define cpucycles_end monotonic_end

static inline uint64_t monotonic_begin(void)
{
  struct timespec ts;
  clock_gettime(CLOCK_MONOTONIC, &ts);
  return ((uint64_t)ts.tv_sec * 1000000000ULL) + ts.tv_nsec;
}

static inline uint64_t monotonic_end(void)
{
  struct timespec ts;
  clock_gettime(CLOCK_MONOTONIC, &ts);
  return ((uint64_t)ts.tv_sec * 1000000000ULL) + ts.tv_nsec;
}
#endif

static int cmp_uint64(const void *a, const void *b)
{
  if(*(uint64_t *)a < *(uint64_t *)b){ return -1; }
  if(*(uint64_t *)a > *(uint64_t *)b){ return 1; }
  return 0;
}

static uint64_t cpucycles_median(uint64_t *l, size_t llen)
{
  qsort(l,llen,sizeof(uint64_t),cmp_uint64);

  if(llen%2) return l[llen/2];
  else return (l[llen/2-1]+l[llen/2])/2;
}

static uint64_t cpucycles_q1(uint64_t *l, size_t llen)
{
  return l[llen/4];
}

static uint64_t cpucycles_q3(uint64_t *l, size_t llen)
{
  return l[(3*llen)/4];
}

#endif
