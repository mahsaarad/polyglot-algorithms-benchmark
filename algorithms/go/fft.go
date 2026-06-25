package main

import (
	"bufio"
	"fmt"
	"math"
	"math/cmplx"
	"os"
	"time"
)

func fft(a []complex128) {
	n := len(a)
	// bit-reversal
	j := 0
	for i := 1; i < n; i++ {
		bit := n >> 1
		for ; j&bit != 0; bit >>= 1 {
			j ^= bit
		}
		j ^= bit
		if i < j {
			a[i], a[j] = a[j], a[i]
		}
	}
	// butterfly
	for length := 2; length <= n; length <<= 1 {
		ang  := 2.0 * math.Pi / float64(length)
		wlen := complex(math.Cos(ang), math.Sin(ang))
		for i := 0; i < n; i += length {
			w := complex(1, 0)
			for jj := 0; jj < length/2; jj++ {
				u := a[i+jj]
				v := a[i+jj+length/2] * w
				a[i+jj]           = u + v
				a[i+jj+length/2]  = u - v
				w *= wlen
			}
		}
	}
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	var n int
	fmt.Fscan(reader, &n)
	a := make([]complex128, n)
	for i := range a {
		var x float64
		fmt.Fscan(reader, &x)
		a[i] = complex(x, 0)
	}

	start := time.Now()
	fft(a)
	ms := float64(time.Since(start).Nanoseconds()) / 1e6

	k   := n
	if k > 5 { k = 5 }
	sum := 0.0
	for i := 0; i < k; i++ { sum += cmplx.Abs(a[i]) }

	fmt.Fprintf(writer, "%.6f\n", sum)
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}