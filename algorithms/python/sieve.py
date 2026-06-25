import sys
import time

def sieve(n):
    is_composite = bytearray(n + 1)  # bytearray خیلی سریع‌تر از list
    is_composite[0] = 1
    if n > 0: is_composite[1] = 1

    i = 2
    while i * i <= n:
        if not is_composite[i]:
            is_composite[i*i::i] = bytes(len(is_composite[i*i::i]))
        i += 1

    count, last = 0, -1
    for k in range(2, n + 1):
        if not is_composite[k]:
            count += 1
            last   = k
    return count, last

def main():
    n = int(sys.stdin.read().strip())

    start        = time.perf_counter()
    count, last  = sieve(n)
    ms           = (time.perf_counter() - start) * 1000

    sys.stdout.write(f"{count}\n{last}\n")
    sys.stderr.write(f"{ms:.3f}\n")

if __name__ == "__main__":
    main()