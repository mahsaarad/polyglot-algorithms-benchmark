#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>

#define NUM_THREADS 4

int n;
long long *A, *B, *C;

typedef struct { int row_start, row_end; } Args;

void *multiply_chunk(void *arg) {
    Args *a = (Args *)arg;
    for (int i = a->row_start; i < a->row_end; i++)
        for (int k = 0; k < n; k++) {
            long long aik = A[i*n + k];
            for (int j = 0; j < n; j++)
                C[i*n + j] += aik * B[k*n + j];
        }
    return NULL;
}

int main() {
    scanf("%d", &n);
    A = malloc(n * n * sizeof(long long));
    B = malloc(n * n * sizeof(long long));
    C = calloc(n * n, sizeof(long long));

    for (int i = 0; i < n * n; i++) scanf("%lld", &A[i]);
    for (int i = 0; i < n * n; i++) scanf("%lld", &B[i]);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    pthread_t threads[NUM_THREADS];
    Args      args[NUM_THREADS];
    int chunk = (n + NUM_THREADS - 1) / NUM_THREADS;

    for (int t = 0; t < NUM_THREADS; t++) {
        args[t].row_start = t * chunk;
        args[t].row_end   = (t+1)*chunk < n ? (t+1)*chunk : n;
        pthread_create(&threads[t], NULL, multiply_chunk, &args[t]);
    }
    for (int t = 0; t < NUM_THREADS; t++)
        pthread_join(threads[t], NULL);

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