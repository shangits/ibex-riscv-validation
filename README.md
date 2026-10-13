# ibex-riscv-validation

Bare-metal test suite for the [ibex](https://github.com/lowRISC/ibex) RISC-V CPU core running on a Verilator simulation. Tests are written in C, compiled with a RISC-V cross compiler, and run on the simulated CPU. The Python harness reads the virtual UART output and reports PASS or FAIL with cycle and instruction counts for each test.

## Tests

| Test | What it checks |
|------|---------------|
| `mem_test` | Writes 5 bit patterns to RAM and reads them back |
| `fib_test` | Computes 10 Fibonacci numbers and compares against known values |
| `overflow_test` | Verifies unsigned wrap, signed overflow, bit shift, and underflow |

## Setup

Requires Docker and a RISC-V cross compiler. The simulation runs inside a Linux container with Verilator built from source.

**1. Clone ibex and this repo**
```bash
git clone https://github.com/lowRISC/ibex.git
git clone https://github.com/shangits/ibex-riscv-validation.git
```

**2. Start a Docker container with ibex mounted**
```bash
docker run -it --rm -v ~/ibex:/ibex ubuntu:22.04
```

**3. Inside the container, build the Verilator simulator**
```bash
cd /ibex
fusesoc --cores-root=. run --target=sim --tool=verilator \
  --verilator_options="-Wno-UNOPTFLAT" lowrisc:ibex:ibex_simple_system
```

**4. Copy test files into place and run**
```bash
cp -r ibex-riscv-validation/* /ibex/
python3 /ibex/run_tests.py
```

## Output

```
==================================================
  ibex RISC-V Validation Harness
==================================================
  mem_test             ... PASS  (0.05s)
    UART        : mem_test: PASS
    Cycles      : 520
    Instructions: 34
  fib_test             ... PASS  (0.04s)
    UART        : fib_test: PASS
    Cycles      : 688
    Instructions: 124
  overflow_test        ... PASS  (0.04s)
    UART        : overflow_test: PASS
    Cycles      : 565
    Instructions: 27
==================================================
  Results: 3/3 passed
==================================================
```