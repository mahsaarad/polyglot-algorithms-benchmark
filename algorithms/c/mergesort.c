#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static int *tmp;

void merge(int *arr, int l, int m, int r) {
    for (int i = l; i <= r; i++) tmp[i] = arr[i];
    int i = l, j = m + 1, k = l;
    while (i <= m && j <= r)
        arr[k++] = tmp[i] <= tmp[j] ? tmp[i++] : tmp[j++];
    while (i <= m) arr[k++] = tmp[i++];
    while (j <= r) arr[k++] = tmp[j++];
}

void mergesort(int *arr, int l, int r) {
    if (l >= r) return;
    int m = l + (r - l) / 2;
    mergesort(arr, l, m);
    mergesort(arr, m + 1, r);
    merge(arr, l, m, r);
}

int main() {
    int n;
    scanf("%d", &n);
    int *arr = malloc(n * sizeof(int));
    tmp     = malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) scanf("%d", &arr[i]);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    mergesort(arr, 0, n - 1);
    clock_gettime(CLOCK_MONOTONIC, &end);

    double ms = (end.tv_sec  - start.tv_sec)  * 1000.0
              + (end.tv_nsec - start.tv_nsec) / 1e6;

    for (int i = 0; i < n; i++)
        printf("%d%c", arr[i], i < n - 1 ? ' ' : '\n');
    fprintf(stderr, "%.3f\n", ms);

    free(arr); free(tmp);
    return 0;
}