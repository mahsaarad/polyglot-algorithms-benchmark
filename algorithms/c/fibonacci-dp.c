#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MOD 1000000007

int main() {
    long long n;
    scanf("%lld", &n);

    long long *memo = calloc(n + 1, sizeof(long long));
    for (long long i = 0; i <= n; i++) memo[i] = -1;
    memo[0] = 0;
    if (n > 0) memo[1] = 1;

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (long long i = 2; i <= n; i++)
        memo[i] = (memo[i-1] + memo[i-2]) % MOD;

    clock_gettime(CLOCK_MONOTONIC, &end);
    double ms = (end.tv_sec  - start.tv_sec)  * 1000.0
              + (end.tv_nsec - start.tv_nsec) / 1e6;

    printf("%lld\n", memo[n]);
    fprintf(stderr, "%.3f\n", ms);

    free(memo);
    return 0;
}