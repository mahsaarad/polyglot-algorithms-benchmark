import sys
import time

def lcg_next(s):
    s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
    return (s >> 1) / (1 << 31), s

def montecarlo(n, seed):
    s      = seed
    inside = 0
    for _ in range(n):
        x, s = lcg_next(s)
        y, s = lcg_next(s)
        if x*x + y*y <= 1.0:
            inside += 1
    return 4.0 * inside / n

def main():
    data = sys.stdin.read().split()
    n    = int(data[0])
    seed = int(data[1])

    start = time.perf_counter()
    pi    = montecarlo(n, seed)
    ms    = (time.perf_counter() - start) * 1000

    sys.stdout.write(f"{pi:.8f}\n")
    sys.stderr.write(f"{ms:.3f}\n")

if __name__ == "__main__":
    main()