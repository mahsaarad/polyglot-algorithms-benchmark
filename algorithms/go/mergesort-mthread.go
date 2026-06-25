package main

import (
	"bufio"
	"fmt"
	"os"
	"runtime"
	"strings"
	"sync"
	"time"
)

func mergeSeq(arr, tmp []int, l, m, r int) {
	copy(tmp[l:r+1], arr[l:r+1])
	i, j, k := l, m+1, l
	for i <= m && j <= r {
		if tmp[i] <= tmp[j] { arr[k] = tmp[i]; i++ } else { arr[k] = tmp[j]; j++ }
		k++
	}
	for ; i <= m; i++ { arr[k] = tmp[i]; k++ }
	for ; j <= r; j++ { arr[k] = tmp[j]; k++ }
}

func mergesortSeq(arr, tmp []int, l, r int) {
	if l >= r { return }
	m := l + (r-l)/2
	mergesortSeq(arr, tmp, l, m)
	mergesortSeq(arr, tmp, m+1, r)
	mergeSeq(arr, tmp, l, m, r)
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	var n int
	fmt.Fscan(reader, &n)
	arr := make([]int, n)
	for i := range arr { fmt.Fscan(reader, &arr[i]) }
	tmp := make([]int, n)

	numCPU := runtime.NumCPU()
	runtime.GOMAXPROCS(numCPU)
	chunk := (n + numCPU - 1) / numCPU

	start := time.Now()

	// هر goroutine یک chunk جداگانه sort می‌کنه
	var wg sync.WaitGroup
	for i := 0; i < numCPU; i++ {
		l := i * chunk
		if l >= n { break }
		r := l + chunk - 1
		if r >= n { r = n - 1 }
		wg.Add(1)
		go func(l, r int) {
			defer wg.Done()
			mergesortSeq(arr, tmp, l, r)
		}(l, r)
	}
	wg.Wait()

	// merge نهایی chunk‌های مرتب‌شده
	for size := chunk; size < n; size *= 2 {
		for l := 0; l < n-size; l += 2 * size {
			m := l + size - 1
			r := l + 2*size - 1
			if r >= n { r = n - 1 }
			mergeSeq(arr, tmp, l, m, r)
		}
	}

	ms := float64(time.Since(start).Nanoseconds()) / 1e6

	sb := make([]string, n)
	for i, v := range arr { sb[i] = fmt.Sprintf("%d", v) }
	fmt.Fprintln(writer, strings.Join(sb, " "))
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}