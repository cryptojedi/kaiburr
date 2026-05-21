#include <stdint.h>
#include <stdio.h>

#include "sample.h"

int randombytes(uint8_t *buf, size_t len);
int sample_f(int n, uint8_t *buf);

int main() {
    int n = 32;

    uint8_t buf[64];

    randombytes(buf, sizeof(buf));

    int result = sample_f(n, buf);

    printf("%d\n", result);

    return 0;
}