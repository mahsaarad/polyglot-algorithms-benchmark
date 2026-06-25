#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int *build_lps(const char *pat, int m) {
    int *lps = calloc(m, sizeof(int));
    int len = 0, i = 1;
    while (i < m) {
        if (pat[i] == pat[len]) { lps[i++] = ++len; }
        else if (len)           { len = lps[len - 1]; }
        else                    { lps[i++] = 0; }
    }
    return lps;
}

int main() {
    char *text = malloc(10000002);
    char *pat  = malloc(102);
    scanf("%s", text);
    scanf("%s", pat);

    int n = strlen(text), m = strlen(pat);
    int *lps     = build_lps(pat, m);
    int *matches = malloc(n * sizeof(int));

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    int count = 0, i = 0, j = 0;
    while (i < n) {
        if (text[i] == pat[j]) { i++; j++; }
        if (j == m) { matches[count++] = i - j; j = lps[j - 1]; }
        else if (i < n && text[i] != pat[j]) {
            if (j) j = lps[j - 1]; else i++;
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double ms = (end.tv_sec  - start.tv_sec)  * 1000.0
              + (end.tv_nsec - start.tv_nsec) / 1e6;

    printf("%d\n", count);
    for (int k = 0; k < count; k++)
        printf("%d%c", matches[k], k < count - 1 ? ' ' : '\n');
    if (count == 0) printf("\n");
    fprintf(stderr, "%.3f\n", ms);

    free(text); free(pat); free(lps); free(matches);
    return 0;
}