import sys
import time

def merge(arr, tmp, l, m, r):
    tmp[l:r+1] = arr[l:r+1]
    i, j, k = l, m + 1, l
    while i <= m and j <= r:
        if tmp[i] <= tmp[j]:
            arr[k] = tmp[i]; i += 1
        else:
            arr[k] = tmp[j]; j += 1
        k += 1
    while i <= m:
        arr[k] = tmp[i]; i += 1; k += 1
    while j <= r:
        arr[k] = tmp[j]; j += 1; k += 1

def mergesort(arr, tmp, l, r):
    if l >= r:
        return
    m = l + (r - l) // 2
    mergesort(arr, tmp, l, m)
    mergesort(arr, tmp, m + 1, r)
    merge(arr, tmp, l, m, r)

def main():
    data = sys.stdin.read().split()
    n    = int(data[0])
    arr  = list(map(int, data[1:n+1]))
    tmp  = [0] * n

    # افزایش recursion limit برای n بزرگ
    sys.setrecursionlimit(n * 2 + 100)

    start  = time.perf_counter()
    mergesort(arr, tmp, 0, n - 1)
    ms = (time.perf_counter() - start) * 1000

    sys.stdout.write(" ".join(map(str, arr)) + "\n")
    sys.stderr.write(f"{ms:.3f}\n")

if __name__ == "__main__":
    main()