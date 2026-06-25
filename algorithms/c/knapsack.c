#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    int W, n;
    scanf("%d %d", &W, &n);

    int *weight = malloc(n * sizeof(int));
    int *value  = malloc(n * sizeof(int));
    for (int i = 0; i < n; i++)
        scanf("%d %d", &weight[i], &value[i]);

    int *dp = calloc(W + 1, sizeof(int));

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 0; i < n; i++)
        for (int w = W; w >= weight[i]; w--) {
            int v = dp[w - weight[i]] + value[i];
            if (v > dp[w]) dp[w] = v;
        }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double ms = (end.tv_sec  - start.tv_sec)  * 1000.0
              + (end.tv_nsec - start.tv_nsec) / 1e6;

    printf("%d\n", dp[W]);
    fprintf(stderr, "%.3f\n", ms);

    free(weight); free(value); free(dp);
    return 0;
}