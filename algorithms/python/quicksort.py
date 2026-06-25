import sys
import time

sys.setrecursionlimit(2000000)

def partition(arr, l, r):
    pivot, i = arr[r], l
    for j in range(l, r):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[r] = arr[r], arr[i]
    return i

def quicksort(arr, l, r):
    if l >= r:
        return
    p = partition(arr, l, r)
    quicksort(arr, l, p - 1)
    quicksort(arr, p + 1, r)

def main():
    data = sys.stdin.read().split()
    n    = int(data[0])
    arr  = list(map(int, data[1:n+1]))

    start = time.perf_counter()
    quicksort(arr, 0, n - 1)
    ms = (time.perf_counter() - start) * 1000

    sys.stdout.write(" ".join(map(str, arr)) + "\n")
    sys.stderr.write(f"{ms:.3f}\n")

if __name__ == "__main__":
    main()