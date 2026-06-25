package main

import (
	"bufio"
	"fmt"
	"os"
	"runtime"
	"sync"
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

	numCPU := runtime.NumCPU()
	runtime.GOMAXPROCS(numCPU)
	chunk := (n + numCPU - 1) / numCPU

	start := time.Now()

	var wg sync.WaitGroup
	for t := 0; t < numCPU; t++ {
		rowStart := t * chunk
		rowEnd   := (t+1) * chunk
		if rowEnd > n { rowEnd = n }
		if rowStart >= n { break }

		wg.Add(1)
		go func(rs, re int) {
			defer wg.Done()
			for i := rs; i < re; i++ {
				for k := 0; k < n; k++ {
					aik := a[i*n+k]
					for j := 0; j < n; j++ {
						c[i*n+j] += aik * b[k*n+j]
					}
				}
			}
		}(rowStart, rowEnd)
	}
	wg.Wait()

	ms := float64(time.Since(start).Nanoseconds()) / 1e6

	var checksum int64
	for _, v := range c { checksum += v }

	fmt.Fprintln(writer, checksum)
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}