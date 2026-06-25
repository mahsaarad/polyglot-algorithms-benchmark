#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

typedef struct { double r, i; } Complex;

static inline Complex cadd(Complex a, Complex b){ return (Complex){a.r+b.r, a.i+b.i}; }
static inline Complex csub(Complex a, Complex b){ return (Complex){a.r-b.r, a.i-b.i}; }
static inline Complex cmul(Complex a, Complex b){
    return (Complex){a.r*b.r - a.i*b.i, a.r*b.i + a.i*b.r};
}
static inline double  cabs2(Complex a){ return sqrt(a.r*a.r + a.i*a.i); }

void fft(Complex *a, int n) {
    /* bit-reversal */
    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) { Complex t = a[i]; a[i] = a[j]; a[j] = t; }
    }
    /* butterfly */
    for (int len = 2; len <= n; len <<= 1) {
        double ang  = 2.0 * M_PI / len;
        Complex wlen = {cos(ang), sin(ang)};
        for (int i = 0; i < n; i += len) {
            Complex w = {1.0, 0.0};
            for (int j = 0; j < len / 2; j++) {
                Complex u = a[i+j];
                Complex v = cmul(a[i+j+len/2], w);
                a[i+j]         = cadd(u, v);
                a[i+j+len/2]   = csub(u, v);
                w = cmul(w, wlen);
            }
        }
    }
}

int main() {
    int n;
    scanf("%d", &n);
    Complex *a = malloc(n * sizeof(Complex));
    for (int i = 0; i < n; i++) { scanf("%lf", &a[i].r); a[i].i = 0.0; }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    fft(a, n);
    clock_gettime(CLOCK_MONOTONIC, &end);

    double ms = (end.tv_sec  - start.tv_sec)  * 1000.0
              + (end.tv_nsec - start.tv_nsec) / 1e6;

    int    k   = n < 5 ? n : 5;
    double sum = 0.0;
    for (int i = 0; i < k; i++) sum += cabs2(a[i]);
    printf("%.6f\n", sum);
    fprintf(stderr, "%.3f\n", ms);

    free(a);
    return 0;
}