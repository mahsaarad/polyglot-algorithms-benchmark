#include <stdio.h>
#include <time.h>

#define MOD 1000000007

int main() {
    long long n;
    scanf("%lld", &n);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    long long a = 0, b = 1;
    for (long long i = 2; i <= n; i++) {
        long long c = (a + b) % MOD;
        a = b; b = c;
    }
    long long result = (n == 0) ? 0 : b;

    clock_gettime(CLOCK_MONOTONIC, &end);
    double ms = (end.tv_sec  - start.tv_sec)  * 1000.0
              + (end.tv_nsec - start.tv_nsec) / 1e6;

    printf("%lld\n", result);
    fprintf(stderr, "%.3f\n", ms);
    return 0;
}