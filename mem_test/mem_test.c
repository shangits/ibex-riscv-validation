/*
 * mem_test.c: Bare-metal memory read/write test for the ibex RISC-V simulator.
 */

#include "simple_system_common.h"

int main(void) {
    // target address in the simple_system RAM region
    volatile uint32_t *mem = (volatile uint32_t *)0x100800;

    // five patterns chosen to catch common bit flip and wiring bugs
    static const uint32_t patterns[5] = {
        0xDEADBEEF, 0xCAFEBABE, 0x00000000, 0xFFFFFFFF, 0xA5A5A5A5
    };

    int pass = 1;

    pcount_enable(0);
    pcount_reset();
    pcount_enable(1);

    // write each pattern to a distinct memory location
    for (int i = 0; i < 5; i++) mem[i] = patterns[i];

    // read back and verify each location matches what was written
    for (int i = 0; i < 5; i++) {
        if (mem[i] != patterns[i]) pass = 0;
    }

    pcount_enable(0);

    if (pass) { puts("mem_test: PASS\n"); }
    else      { puts("mem_test: FAIL\n"); }

    return 0;
}