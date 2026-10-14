#!/usr/bin/env python3
# run_tests.py: builds and runs each bare-metal test on the ibex simulator,
# checks UART output for PASS/FAIL, and prints cycle and instruction counts.

import subprocess
import os
import sys
import time

IBEX_ROOT = os.path.dirname(os.path.abspath(__file__))
SIMULATOR = os.path.join(IBEX_ROOT, "build/lowrisc_ibex_ibex_simple_system_0/sim-verilator/Vibex_simple_system")
TESTS_DIR = os.path.join(IBEX_ROOT, "examples/sw/simple_system")
UART_LOG  = os.path.join(IBEX_ROOT, "ibex_simple_system.log")

TESTS = ["mem_test", "fib_test", "overflow_test"]


def build_test(test_name):
    # cross-compile the C source into a RISC-V ELF
    test_dir = os.path.join(TESTS_DIR, test_name)
    result = subprocess.run(
        ["make", "-C", test_dir],
        capture_output=True, text=True
    )
    return result.returncode == 0, result.stderr


def run_test(test_name):
    # load the ELF into the simulator and collect output
    elf = os.path.join(TESTS_DIR, test_name, f"{test_name}.elf")

    # delete old log first so we dont read the last test's output
    if os.path.exists(UART_LOG):
        os.remove(UART_LOG)

    result = subprocess.run(
        [SIMULATOR, f"--meminit=ram,{elf}"],
        capture_output=True, text=True,
        cwd=IBEX_ROOT, timeout=30
    )

    # the simulator redirects UART output to a log file instead of stdout
    uart = ""
    if os.path.exists(UART_LOG):
        with open(UART_LOG) as f:
            uart = f.read().strip()

    # parse cycle and instruction counts from simulator stdout
    stats = {}
    for line in result.stdout.splitlines():
        if "Executed cycles:" in line:
            stats["cycles"] = line.split(":")[1].strip()
        if "Instructions Retired:" in line:
            stats["instructions"] = line.split(":")[1].strip()

    return uart, stats


def main():
    print("=" * 50)
    print("  ibex RISC-V Validation Harness")
    print("=" * 50)

    results = []
    for test in TESTS:
        # print test name immediately so progress is visible while it runs
        sys.stdout.write(f"  {test:<20} ... ")
        sys.stdout.flush()

        # build phase
        ok, build_err = build_test(test)
        if not ok:
            print("BUILD FAIL")
            print(build_err)
            results.append((test, "BUILD FAIL"))
            continue

        # run phase
        start = time.time()
        uart, stats = run_test(test)
        elapsed = time.time() - start

        # determine pass/fail from UART output
        if "PASS" in uart:
            status = "PASS"
        elif "FAIL" in uart:
            status = "FAIL"
        else:
            status = "NO OUTPUT"

        # print result and stats for this test
        print(f"{status}  ({elapsed:.2f}s)")
        print(f"    UART        : {uart if uart else '(none)'}")
        print(f"    Cycles      : {stats.get('cycles', 'N/A')}")
        print(f"    Instructions: {stats.get('instructions', 'N/A')}")

        results.append((test, status))

    # final summary
    print("=" * 50)
    passed = sum(1 for _, r in results if r == "PASS")
    print(f"  Results: {passed}/{len(TESTS)} passed")
    print("=" * 50)

    return 0 if passed == len(TESTS) else 1


if __name__ == "__main__":
    sys.exit(main())