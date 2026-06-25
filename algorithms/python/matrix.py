import sys
import time

def matmul(A, B, n):
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            aik = A[i][k]
            for j in range(n):
                C[i][j] += aik * B[k][j]
    return C

def main():
    data = sys.stdin.read().split()
    idx  = 0
    n    = int(data[idx]); idx += 1

    A = []
    for i in range(n):
        row = [int(data[idx+j]) for j in range(n)]
        A.append(row); idx += n

    B = []
    for i in range(n):
        row = [int(data[idx+j]) for j in range(n)]
        B.append(row); idx += n

    start = time.perf_counter()
    C     = matmul(A, B, n)
    ms    = (time.perf_counter() - start) * 1000

    checksum = sum(C[i][j] for i in range(n) for j in range(n))
    sys.stdout.write(f"{checksum}\n")
    sys.stderr.write(f"{ms:.3f}\n")

if __name__ == "__main__":
    main()