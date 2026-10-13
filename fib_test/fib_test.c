/*
 * fib_test.c: Computes the first 10 Fibonacci numbers and checks them
 * against known values to verify arithmetic and branching on ibex.
 */

#include "simple_system_common.h"

// expected fibonacci values in flash 
static const uint32_t FIB_EXPECTED[10] = {0, 1, 1, 2, 3, 5, 8, 13, 21, 34};

int main(void) {
    uint32_t fib[10];
    int pass = 1;

    pcount_enable(0);
    pcount_reset();
    pcount_enable(1);

    // set the first two values
    fib[0] = 0; fib[1] = 1;

    // compute sequence
    for (int i = 2; i < 10; i++) {
        fib[i] = fib[i-1] + fib[i-2];
    }

    // check each result against expected
    for (int i = 0; i < 10; i++) {
        if (fib[i] != FIB_EXPECTED[i]) pass = 0;
    }

    pcount_enable(0);

    if (pass) { puts("fib_test: PASS\n"); }
    else      { puts("fib_test: FAIL\n"); }

    return 0;
}