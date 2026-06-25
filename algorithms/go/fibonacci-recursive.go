package main

import (
	"bufio"
	"fmt"
	"os"
	"time"
)

const MOD = 1_000_000_007

func fib(n int) int {
	if n <= 1 { return n }
	return (fib(n-1) + fib(n-2)) % MOD
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	var n int
	fmt.Fscan(reader, &n)

	start  := time.Now()
	result := fib(n)
	ms     := float64(time.Since(start).Nanoseconds()) / 1e6

	fmt.Fprintln(writer, result)
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}