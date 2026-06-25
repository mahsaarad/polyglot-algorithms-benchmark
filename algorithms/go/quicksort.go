package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"time"
)

func partition(arr []int, l, r int) int {
	pivot, i := arr[r], l
	for j := l; j < r; j++ {
		if arr[j] <= pivot {
			arr[i], arr[j] = arr[j], arr[i]
			i++
		}
	}
	arr[i], arr[r] = arr[r], arr[i]
	return i
}

func quicksort(arr []int, l, r int) {
	if l >= r { return }
	p := partition(arr, l, r)
	quicksort(arr, l, p-1)
	quicksort(arr, p+1, r)
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	var n int
	fmt.Fscan(reader, &n)
	arr := make([]int, n)
	for i := range arr { fmt.Fscan(reader, &arr[i]) }

	start := time.Now()
	quicksort(arr, 0, n-1)
	ms := float64(time.Since(start).Nanoseconds()) / 1e6

	sb := make([]string, n)
	for i, v := range arr { sb[i] = fmt.Sprintf("%d", v) }
	fmt.Fprintln(writer, strings.Join(sb, " "))
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}