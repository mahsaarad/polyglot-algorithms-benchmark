package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"time"
)

func buildLPS(pat string) []int {
	m   := len(pat)
	lps := make([]int, m)
	len_, i := 0, 1
	for i < m {
		if pat[i] == pat[len_] {
			len_++
			lps[i] = len_
			i++
		} else if len_ > 0 {
			len_ = lps[len_-1]
		} else {
			lps[i] = 0
			i++
		}
	}
	return lps
}

func kmp(text, pat string) []int {
	n, m := len(text), len(pat)
	if m == 0 { return nil }
	lps     := buildLPS(pat)
	matches := []int{}
	i, j   := 0, 0
	for i < n {
		if text[i] == pat[j] { i++; j++ }
		if j == m {
			matches = append(matches, i-j)
			j = lps[j-1]
		} else if i < n && text[i] != pat[j] {
			if j > 0 { j = lps[j-1] } else { i++ }
		}
	}
	return matches
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	text, _ := reader.ReadString('\n')
	pat,  _  := reader.ReadString('\n')
	text = strings.TrimSpace(text)
	pat  = strings.TrimSpace(pat)

	start   := time.Now()
	matches := kmp(text, pat)
	ms      := float64(time.Since(start).Nanoseconds()) / 1e6

	fmt.Fprintln(writer, len(matches))
	if len(matches) == 0 {
		fmt.Fprintln(writer)
	} else {
		sb := make([]string, len(matches))
		for i, v := range matches { sb[i] = fmt.Sprintf("%d", v) }
		fmt.Fprintln(writer, strings.Join(sb, " "))
	}
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}