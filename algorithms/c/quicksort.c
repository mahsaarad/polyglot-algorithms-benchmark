#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void swap(int *a, int *b) { int t = *a; *a = *b; *b = t; }

int partition(int *arr, int l, int r) {
    int pivot = arr[r], i = l - 1;
    for (int j = l; j < r; j++)
        if (arr[j] <= pivot) swap(&arr[++i], &arr[j]);
    swap(&arr[i + 1], &arr[r]);
    return i + 1;
}

void quicksort(int *arr, int l, int r) {
    if (l >= r) return;
    int p = partition(arr, l, r);
    quicksort(arr, l, p - 1);
    quicksort(arr, p + 1, r);
}

int main() {
    int n;
    scanf("%d", &n);
    int *arr = malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) scanf("%d", &arr[i]);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    quicksort(arr, 0, n - 1);
    clock_gettime(CLOCK_MONOTONIC, &end);

    double ms = (end.tv_sec  - start.tv_sec)  * 1000.0
              + (end.tv_nsec - start.tv_nsec) / 1e6;

    for (int i = 0; i < n; i++)
        printf("%d%c", arr[i], i < n - 1 ? ' ' : '\n');
    fprintf(stderr, "%.3f\n", ms);

    free(arr);
    return 0;
}