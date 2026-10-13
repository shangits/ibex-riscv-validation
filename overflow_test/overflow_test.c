/*
 * overflow_test.c: Tests integer overflow and underflow behavior on ibex.
 */

#include "simple_system_common.h"

int main(void) {
    int pass = 1;

    pcount_enable(0);
    pcount_reset();
    pcount_enable(1);

    // unsigned max + 1 should wrap to zero
    volatile uint32_t max = 0xFFFFFFFF;
    volatile uint32_t wrapped = max + 1;
    if (wrapped != 0x00000000) pass = 0;

    // signed max + 1 should wrap to most negative value
    volatile int32_t smax = 0x7FFFFFFF;
    volatile int32_t soverflow = smax + 1;
    if (soverflow != (int32_t)0x80000000) pass = 0;

    // shift 1 left by 31 bits to set only the sign bit
    volatile uint32_t shifted = 1u << 31;
    if (shifted != 0x80000000) pass = 0;

    // subtracting 1 from zero should wrap to max unsigned value
    volatile uint32_t zero = 0;
    volatile uint32_t underflow = zero - 1;
    if (underflow != 0xFFFFFFFF) pass = 0;

    pcount_enable(0);

    if (pass) { puts("overflow_test: PASS\n"); }
    else      { puts("overflow_test: FAIL\n"); }

    return 0;
}