#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>

#define NUM_THREADS 4

static int *tmp;

void merge(int *arr, int l, int m, int r) {
    for (int i = l; i <= r; i++) tmp[i] = arr[i];
    int i = l, j = m + 1, k = l;
    while (i <= m && j <= r)
        arr[k++] = tmp[i] <= tmp[j] ? tmp[i++] : tmp[j++];
    while (i <= m) arr[k++] = tmp[i++];
    while (j <= r) arr[k++] = tmp[j++];
}

void mergesort_seq(int *arr, int l, int r) {
    if (l >= r) return;
    int m = l + (r - l) / 2;
    mergesort_seq(arr, l, m);
    mergesort_seq(arr, m + 1, r);
    merge(arr, l, m, r);
}

typedef struct { int *arr; int l, r; } Args;

void *thread_fn(void *arg) {
    Args *a = (Args *)arg;
    mergesort_seq(a->arr, a->l, a->r);
    return NULL;
}

int main() {
    int n;
    scanf("%d", &n);
    int *arr = malloc(n * sizeof(int));
    tmp      = malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) scanf("%d", &arr[i]);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    pthread_t threads[NUM_THREADS];
    Args      args[NUM_THREADS];
    int chunk = n / NUM_THREADS;

    for (int t = 0; t < NUM_THREADS; t++) {
        args[t].arr = arr;
        args[t].l   = t * chunk;
        args[t].r   = (t == NUM_THREADS - 1) ? n - 1 : args[t].l + chunk - 1;
        pthread_create(&threads[t], NULL, thread_fn, &args[t]);
    }
    for (int t = 0; t < NUM_THREADS; t++) pthread_join(threads[t], NULL);

    /* merge sorted chunks پشت سر هم */
    for (int size = chunk; size < n; size *= 2)
        for (int l = 0; l < n - size; l += 2 * size) {
            int m = l + size - 1;
            int r = (l + 2 * size - 1 < n - 1) ? l + 2 * size - 1 : n - 1;
            merge(arr, l, m, r);
        }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double ms = (end.tv_sec  - start.tv_sec)  * 1000.0
              + (end.tv_nsec - start.tv_nsec) / 1e6;

    for (int i = 0; i < n; i++)
        printf("%d%c", arr[i], i < n - 1 ? ' ' : '\n');
    fprintf(stderr, "%.3f\n", ms);

    free(arr); free(tmp);
    return 0;
}