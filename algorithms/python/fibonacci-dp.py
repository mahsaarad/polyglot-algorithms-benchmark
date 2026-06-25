import sys
import time

MOD = 1_000_000_007

def fib_dp(n):
    memo = [0] * (n + 1)
    if n >= 1: memo[1] = 1
    for i in range(2, n + 1):
        memo[i] = (memo[i-1] + memo[i-2]) % MOD
    return memo[n]

def main():
    n = int(sys.stdin.read().strip())

    start  = time.perf_counter()
    result = fib_dp(n)
    ms     = (time.perf_counter() - start) * 1000

    sys.stdout.write(f"{result}\n")
    sys.stderr.write(f"{ms:.3f}\n")

if __name__ == "__main__":
    main()