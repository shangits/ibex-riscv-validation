# ibex-riscv-validation

![CI](https://github.com/shangits/ibex-riscv-validation/actions/workflows/ci.yml/badge.svg)

Bare-metal test suite for the [ibex](https://github.com/lowRISC/ibex) RISC-V CPU core running on a Verilator simulation. Tests are written in C, compiled with a RISC-V cross compiler, and run on the simulated CPU. The Python harness reads the virtual UART output and reports PASS or FAIL with cycle and instruction counts for each test.

## Tests

| Test | What it checks |
|------|---------------|
| `mem_test` | Writes 5 bit patterns to RAM and reads them back |
| `fib_test` | Computes 10 Fibonacci numbers and compares against known values |
| `overflow_test` | Verifies unsigned wrap, signed overflow, bit shift, and underflow |

## CI

Every push runs the full thing on GitHub Actions (see `.github/workflows/ci.yml`). It grabs a pinned ibex commit, installs lowRISC's prebuilt Verilator 4.210 and rv32 toolchain, builds the simulator, drops the tests into ibex and runs `run_tests.py`. The built simulator is cached so later runs skip that step.

Versions are pinned on purpose so a red run means my change broke something, not an ibex or tool update.

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

The tests go next to ibex's own hello_test so the Makefiles can find `../common/common.mk`. Run this on your machine (not in the container):
```bash
cp -r ibex-riscv-validation/mem_test ibex-riscv-validation/fib_test ibex-riscv-validation/overflow_test ~/ibex/examples/sw/simple_system/
cp ibex-riscv-validation/run_tests.py ~/ibex/
```
Then inside the container:
```bash
python3 /ibex/run_tests.py
```

## Output

```
==================================================
  ibex RISC-V Validation Harness
==================================================
  mem_test             ... PASS  (0.05s)
    UART        : mem_test: PASS
    Cycles      : 521
    Instructions: 35
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