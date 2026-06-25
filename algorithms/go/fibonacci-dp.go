package main

import (
	"bufio"
	"fmt"
	"os"
	"time"
)

const MOD = 1_000_000_007

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	var n int
	fmt.Fscan(reader, &n)

	start := time.Now()

	memo := make([]int64, n+1)
	if n > 0 { memo[1] = 1 }
	for i := 2; i <= n; i++ {
		memo[i] = (memo[i-1] + memo[i-2]) % MOD
	}

	ms := float64(time.Since(start).Nanoseconds()) / 1e6

	fmt.Fprintln(writer, memo[n])
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}