import sys
import time

def lcs(a, b):
    n, m = len(a), len(b)
    prev = [0] * (m + 1)
    curr = [0] * (m + 1)

    for i in range(1, n + 1):
        ai = a[i-1]
        for j in range(1, m + 1):
            if ai == b[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = curr[j-1] if curr[j-1] > prev[j] else prev[j]
        prev, curr = curr, prev
        for j in range(m + 1): curr[j] = 0

    return prev[m]

def main():
    data   = sys.stdin.read().splitlines()
    a      = data[0].strip()
    b      = data[1].strip()

    start  = time.perf_counter()
    result = lcs(a, b)
    ms     = (time.perf_counter() - start) * 1000

    sys.stdout.write(f"{result}\n")
    sys.stderr.write(f"{ms:.3f}\n")

if __name__ == "__main__":
    main()