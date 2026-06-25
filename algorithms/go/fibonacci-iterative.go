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

	var n int64
	fmt.Fscan(reader, &n)

	start := time.Now()

	var result int64
	if n == 0 {
		result = 0
	} else {
		a, b := int64(0), int64(1)
		for i := int64(2); i <= n; i++ {
			c := (a + b) % MOD
			a = b; b = c
		}
		result = b
	}

	ms := float64(time.Since(start).Nanoseconds()) / 1e6

	fmt.Fprintln(writer, result)
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}