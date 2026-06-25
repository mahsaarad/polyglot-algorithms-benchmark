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

	var W, n int
	fmt.Fscan(reader, &W, &n)

	weight := make([]int, n)
	value  := make([]int, n)
	for i := 0; i < n; i++ {
		fmt.Fscan(reader, &weight[i], &value[i])
	}

	start := time.Now()

	dp := make([]int, W+1)
	for i := 0; i < n; i++ {
		for w := W; w >= weight[i]; w-- {
			if v := dp[w-weight[i]] + value[i]; v > dp[w] {
				dp[w] = v
			}
		}
	}

	ms := float64(time.Since(start).Nanoseconds()) / 1e6

	fmt.Fprintln(writer, dp[W])
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}