#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    long long n;
    unsigned int seed;
    scanf("%lld %u", &n, &seed);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    unsigned int s = seed;
    long long inside = 0;
    for (long long i = 0; i < n; i++) {
        /* LCG fast random — همان seed در همه زبان‌ها */
        s = s * 1664525u + 1013904223u;
        double x = (s >> 1) / (double)(1u << 31);
        s = s * 1664525u + 1013904223u;
        double y = (s >> 1) / (double)(1u << 31);
        if (x*x + y*y <= 1.0) inside++;
    }

    double pi = 4.0 * inside / n;

    clock_gettime(CLOCK_MONOTONIC, &end);
    double ms = (end.tv_sec  - start.tv_sec)  * 1000.0
              + (end.tv_nsec - start.tv_nsec) / 1e6;

    printf("%.8f\n", pi);
    fprintf(stderr, "%.3f\n", ms);
    return 0;
}