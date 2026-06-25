import sys
import time
import math

def fft(a):
    n = len(a)
    # bit-reversal
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    # butterfly
    length = 2
    while length <= n:
        ang  = 2 * math.pi / length
        wlen = complex(math.cos(ang), math.sin(ang))
        for i in range(0, n, length):
            w = complex(1, 0)
            for jj in range(length // 2):
                u = a[i + jj]
                v = a[i + jj + length // 2] * w
                a[i + jj]              = u + v
                a[i + jj + length // 2] = u - v
                w *= wlen
        length <<= 1

def main():
    data = sys.stdin.read().split()
    idx  = 0
    n    = int(data[idx]); idx += 1
    a    = [complex(float(data[idx + i]), 0) for i in range(n)]

    start = time.perf_counter()
    fft(a)
    ms = (time.perf_counter() - start) * 1000

    k   = min(5, n)
    s   = sum(abs(a[i]) for i in range(k))
    sys.stdout.write(f"{s:.6f}\n")
    sys.stderr.write(f"{ms:.3f}\n")

if __name__ == "__main__":
    main()