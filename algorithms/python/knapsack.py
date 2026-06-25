import sys
import time

def knapsack(W, weights, values, n):
    dp = [0] * (W + 1)
    for i in range(n):
        wi, vi = weights[i], values[i]
        for w in range(W, wi - 1, -1):
            candidate = dp[w - wi] + vi
            if candidate > dp[w]:
                dp[w] = candidate
    return dp[W]

def main():
    data  = sys.stdin.read().split()
    idx   = 0
    W     = int(data[idx]); idx += 1
    n     = int(data[idx]); idx += 1

    weights = []
    values  = []
    for _ in range(n):
        weights.append(int(data[idx])); idx += 1
        values.append(int(data[idx]));  idx += 1

    start  = time.perf_counter()
    result = knapsack(W, weights, values, n)
    ms     = (time.perf_counter() - start) * 1000

    sys.stdout.write(f"{result}\n")
    sys.stderr.write(f"{ms:.3f}\n")

if __name__ == "__main__":
    main()