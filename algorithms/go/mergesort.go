package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"time"
)

var tmp []int

func merge(arr []int, l, m, r int) {
	copy(tmp[l:r+1], arr[l:r+1])
	i, j, k := l, m+1, l
	for i <= m && j <= r {
		if tmp[i] <= tmp[j] {
			arr[k] = tmp[i]; i++
		} else {
			arr[k] = tmp[j]; j++
		}
		k++
	}
	for ; i <= m; i++ { arr[k] = tmp[i]; k++ }
	for ; j <= r; j++ { arr[k] = tmp[j]; k++ }
}

func mergesort(arr []int, l, r int) {
	if l >= r { return }
	m := l + (r-l)/2
	mergesort(arr, l, m)
	mergesort(arr, m+1, r)
	merge(arr, l, m, r)
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	var n int
	fmt.Fscan(reader, &n)
	arr := make([]int, n)
	for i := range arr { fmt.Fscan(reader, &arr[i]) }
	tmp = make([]int, n)

	start := time.Now()
	mergesort(arr, 0, n-1)
	ms := float64(time.Since(start).Nanoseconds()) / 1e6

	sb := make([]string, n)
	for i, v := range arr { sb[i] = fmt.Sprintf("%d", v) }
	fmt.Fprintln(writer, strings.Join(sb, " "))
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}