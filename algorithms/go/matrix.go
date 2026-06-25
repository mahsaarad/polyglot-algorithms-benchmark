package main

import (
	"bufio"
	"fmt"
	"os"
	"time"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	var n int
	fmt.Fscan(reader, &n)
	size := n * n

	a := make([]int64, size)
	b := make([]int64, size)
	c := make([]int64, size)

	for i := range a { fmt.Fscan(reader, &a[i]) }
	for i := range b { fmt.Fscan(reader, &b[i]) }

	start := time.Now()

	for i := 0; i < n; i++ {
		for k := 0; k < n; k++ {
			aik := a[i*n+k]
			for j := 0; j < n; j++ {
				c[i*n+j] += aik * b[k*n+j]
			}
		}
	}

	ms := float64(time.Since(start).Nanoseconds()) / 1e6

	var checksum int64
	for _, v := range c { checksum += v }

	fmt.Fprintln(writer, checksum)
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}