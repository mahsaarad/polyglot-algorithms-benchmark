import sys
import time

MOD = 1_000_000_007

def fib(n):
    if n <= 1: return n
    return (fib(n-1) + fib(n-2)) % MOD

def main():
    n = int(sys.stdin.read().strip())
    sys.setrecursionlimit(100000)

    start  = time.perf_counter()
    result = fib(n)
    ms     = (time.perf_counter() - start) * 1000

    sys.stdout.write(f"{result}\n")
    sys.stderr.write(f"{ms:.3f}\n")

if __name__ == "__main__":
    main()