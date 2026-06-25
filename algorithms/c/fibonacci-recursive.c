#include <stdio.h>
#include <time.h>

#define MOD 1000000007

long long fib(int n) {
    if (n <= 1) return n;
    return (fib(n-1) + fib(n-2)) % MOD;
}

int main() {
    int n;
    scanf("%d", &n);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    long long result = fib(n);
    clock_gettime(CLOCK_MONOTONIC, &end);

    double ms = (end.tv_sec  - start.tv_sec)  * 1000.0
              + (end.tv_nsec - start.tv_nsec) / 1e6;

    printf("%lld\n", result);
    fprintf(stderr, "%.3f\n", ms);
    return 0;
}