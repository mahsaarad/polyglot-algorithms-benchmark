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

	start := time.Now()

	isComposite := make([]bool, n+1)
	isComposite[0] = true
	if n > 0 { isComposite[1] = true }

	for i := 2; i*i <= n; i++ {
		if !isComposite[i] {
			for j := i * i; j <= n; j += i {
				isComposite[j] = true
			}
		}
	}

	var count, last int64
	for k := 2; k <= n; k++ {
		if !isComposite[k] {
			count++
			last = int64(k)
		}
	}

	ms := float64(time.Since(start).Nanoseconds()) / 1e6

	fmt.Fprintln(writer, count)
	fmt.Fprintln(writer, last)
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}