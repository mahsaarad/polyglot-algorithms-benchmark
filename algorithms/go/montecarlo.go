package main

import (
	"bufio"
	"fmt"
	"os"
	"time"
)

func lcgNext(s *uint32) float64 {
	*s = *s*1664525 + 1013904223
	return float64(*s>>1) / float64(uint32(1)<<31)
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	var n    int64
	var seed uint32
	fmt.Fscan(reader, &n, &seed)

	start := time.Now()

	s      := seed
	inside := int64(0)
	for i := int64(0); i < n; i++ {
		x := lcgNext(&s)
		y := lcgNext(&s)
		if x*x+y*y <= 1.0 { inside++ }
	}
	pi := 4.0 * float64(inside) / float64(n)

	ms := float64(time.Since(start).Nanoseconds()) / 1e6

	fmt.Fprintf(writer, "%.8f\n", pi)
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}