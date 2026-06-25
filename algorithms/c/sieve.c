#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main() {
    long long n;
    scanf("%lld", &n);

    // bitset برای کاهش مصرف RAM
    unsigned char *is_composite = calloc((n + 1), sizeof(unsigned char));

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    is_composite[0] = is_composite[1] = 1;
    for (long long i = 2; i * i <= n; i++) {
        if (!is_composite[i]) {
            for (long long j = i * i; j <= n; j += i)
                is_composite[j] = 1;
        }
    }

    long long count = 0, last = -1;
    for (long long i = 2; i <= n; i++) {
        if (!is_composite[i]) { count++; last = i; }
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double ms = (end.tv_sec  - start.tv_sec)  * 1000.0
              + (end.tv_nsec - start.tv_nsec) / 1e6;

    printf("%lld\n%lld\n", count, last);
    fprintf(stderr, "%.3f\n", ms);

    free(is_composite);
    return 0;
}