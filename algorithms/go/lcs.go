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

	var a, b string
	fmt.Fscan(reader, &a)
	fmt.Fscan(reader, &b)
	n, m := len(a), len(b)

	start := time.Now()

	prev := make([]int, m+1)
	curr := make([]int, m+1)

	for i := 1; i <= n; i++ {
		for j := 1; j <= m; j++ {
			if a[i-1] == b[j-1] {
				curr[j] = prev[j-1] + 1
			} else if curr[j-1] > prev[j] {
				curr[j] = curr[j-1]
			} else {
				curr[j] = prev[j]
			}
		}
		prev, curr = curr, prev
		for k := range curr { curr[k] = 0 }
	}

	ms := float64(time.Since(start).Nanoseconds()) / 1e6

	fmt.Fprintln(writer, prev[m])
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}