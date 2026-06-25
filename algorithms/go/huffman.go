package main

import (
	"bufio"
	"container/heap"
	"fmt"
	"os"
	"time"
)

type Node struct {
	freq        int
	ch          byte
	left, right *Node
}

type PQ []*Node

func (pq PQ) Len() int            { return len(pq) }
func (pq PQ) Less(i, j int) bool  { return pq[i].freq < pq[j].freq }
func (pq PQ) Swap(i, j int)       { pq[i], pq[j] = pq[j], pq[i] }
func (pq *PQ) Push(x interface{}) { *pq = append(*pq, x.(*Node)) }
func (pq *PQ) Pop() interface{} {
	old := *pq; n := len(old)
	x := old[n-1]; *pq = old[:n-1]
	return x
}

var codes [256]int

func buildCodes(n *Node, depth int) {
	if n == nil { return }
	if n.left == nil && n.right == nil {
		if depth == 0 { depth = 1 }
		codes[n.ch] = depth
		return
	}
	buildCodes(n.left,  depth+1)
	buildCodes(n.right, depth+1)
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	var text string
	fmt.Fscan(reader, &text)
	n := len(text)

	var freq [256]int
	for i := 0; i < n; i++ { freq[text[i]]++ }

	start := time.Now()

	pq := &PQ{}
	heap.Init(pq)
	unique := 0
	for ch, f := range freq {
		if f > 0 {
			heap.Push(pq, &Node{freq: f, ch: byte(ch)})
			unique++
		}
	}

	for pq.Len() > 1 {
		l := heap.Pop(pq).(*Node)
		r := heap.Pop(pq).(*Node)
		heap.Push(pq, &Node{freq: l.freq + r.freq, left: l, right: r})
	}

	if pq.Len() > 0 {
		buildCodes(heap.Pop(pq).(*Node), 0)
	}

	totalBits := 0
	for ch, f := range freq {
		if f > 0 { totalBits += f * codes[ch] }
	}

	ms    := float64(time.Since(start).Nanoseconds()) / 1e6
	ratio := float64(totalBits) / (8.0 * float64(n))

	fmt.Fprintln(writer, unique)
	fmt.Fprintln(writer, totalBits)
	fmt.Fprintf(writer, "%.2f\n", ratio)
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}