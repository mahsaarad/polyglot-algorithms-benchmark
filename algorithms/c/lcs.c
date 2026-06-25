#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main() {
    char *a = malloc(5001);
    char *b = malloc(5001);
    scanf("%s", a);
    scanf("%s", b);

    int n = strlen(a), m = strlen(b);

    /* فقط دو ردیف — بهینه RAM */
    int *prev = calloc(m + 1, sizeof(int));
    int *curr = calloc(m + 1, sizeof(int));

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (a[i-1] == b[j-1])
                curr[j] = prev[j-1] + 1;
            else
                curr[j] = curr[j-1] > prev[j] ? curr[j-1] : prev[j];
        }
        int *tmp = prev; prev = curr; curr = tmp;
        memset(curr, 0, (m + 1) * sizeof(int));
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double ms = (end.tv_sec  - start.tv_sec)  * 1000.0
              + (end.tv_nsec - start.tv_nsec) / 1e6;

    printf("%d\n", prev[m]);
    fprintf(stderr, "%.3f\n", ms);

    free(a); free(b); free(prev); free(curr);
    return 0;
}