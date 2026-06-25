#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    int n;
    scanf("%d", &n);

    long long *A = malloc(n * n * sizeof(long long));
    long long *B = malloc(n * n * sizeof(long long));
    long long *C = calloc(n * n, sizeof(long long));

    for (int i = 0; i < n * n; i++) scanf("%lld", &A[i]);
    for (int i = 0; i < n * n; i++) scanf("%lld", &B[i]);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 0; i < n; i++)
        for (int k = 0; k < n; k++) {        /* cache-friendly loop order */
            long long aik = A[i*n + k];
            for (int j = 0; j < n; j++)
                C[i*n + j] += aik * B[k*n + j];
        }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double ms = (end.tv_sec  - start.tv_sec)  * 1000.0
              + (end.tv_nsec - start.tv_nsec) / 1e6;

    long long checksum = 0;
    for (int i = 0; i < n * n; i++) checksum += C[i];

    printf("%lld\n", checksum);
    fprintf(stderr, "%.3f\n", ms);

    free(A); free(B); free(C);
    return 0;
}