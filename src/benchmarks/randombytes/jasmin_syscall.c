#include "jasmin_syscall.h"

#include <stdint.h>
#include <unistd.h>
#include <sys/random.h>

uint8_t* __jasmin_syscall_randombytes__(uint8_t* _x, uint64_t xlen)
{
  int i;
  uint8_t* x = _x;

  while (xlen > 0) {
    if (xlen < 1048576) i = xlen; else i = 1048576;

    i = getrandom(x, i, 0);
    if (i < 1) {
      sleep(1);
      continue;
    }
    x += i;
    xlen -= i;
  }

  return _x;
}
