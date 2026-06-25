import sys
import time

MOD = 1_000_000_007

def fib_iterative(n):
    if n == 0: return 0
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, (a + b) % MOD
    return b

def main():
    n = int(sys.stdin.read().strip())

    start  = time.perf_counter()
    result = fib_iterative(n)
    ms     = (time.perf_counter() - start) * 1000

    sys.stdout.write(f"{result}\n")
    sys.stderr.write(f"{ms:.3f}\n")

if __name__ == "__main__":
    main()