package main

import (
	"bufio"
	"container/heap"
	"fmt"
	"os"
	"time"
)

const INF = 1_000_000_000

type Edge struct{ to, w int }
type Item struct{ dist, node int }
type PQ []Item

func (pq PQ) Len() int            { return len(pq) }
func (pq PQ) Less(i, j int) bool  { return pq[i].dist < pq[j].dist }
func (pq PQ) Swap(i, j int)       { pq[i], pq[j] = pq[j], pq[i] }
func (pq *PQ) Push(x interface{}) { *pq = append(*pq, x.(Item)) }
func (pq *PQ) Pop() interface{} {
	old := *pq; n := len(old)
	x := old[n-1]; *pq = old[:n-1]
	return x
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	var V, E, src int
	fmt.Fscan(reader, &V, &E, &src)

	graph := make([][]Edge, V)
	for i := 0; i < E; i++ {
		var u, to, w int
		fmt.Fscan(reader, &u, &to, &w)
		graph[u] = append(graph[u], Edge{to, w})
	}

	start := time.Now()

	dist := make([]int, V)
	for i := range dist { dist[i] = INF }
	dist[src] = 0

	pq := &PQ{{0, src}}
	heap.Init(pq)

	for pq.Len() > 0 {
		cur := heap.Pop(pq).(Item)
		if cur.dist > dist[cur.node] { continue }
		for _, e := range graph[cur.node] {
			nd := cur.dist + e.w
			if nd < dist[e.to] {
				dist[e.to] = nd
				heap.Push(pq, Item{nd, e.to})
			}
		}
	}

	ms := float64(time.Since(start).Nanoseconds()) / 1e6

	for i, d := range dist {
		if i > 0 { fmt.Fprint(writer, " ") }
		if d == INF { fmt.Fprint(writer, -1) } else { fmt.Fprint(writer, d) }
	}
	fmt.Fprintln(writer)
	fmt.Fprintf(os.Stderr, "%.3f\n", ms)
}