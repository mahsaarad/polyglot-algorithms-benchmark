import sys
import time
import heapq

INF = float('inf')

def dijkstra(graph, V, src):
    dist = [INF] * V
    dist[src] = 0
    heap = [(0, src)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for to, w in graph[u]:
            nd = d + w
            if nd < dist[to]:
                dist[to] = nd
                heapq.heappush(heap, (nd, to))
    return dist

def main():
    data = sys.stdin.read().split()
    idx  = 0
    V    = int(data[idx]); idx += 1
    E    = int(data[idx]); idx += 1
    src  = int(data[idx]); idx += 1

    graph = [[] for _ in range(V)]
    for _ in range(E):
        u = int(data[idx]); idx += 1
        t = int(data[idx]); idx += 1
        w = int(data[idx]); idx += 1
        graph[u].append((t, w))

    start = time.perf_counter()
    dist  = dijkstra(graph, V, src)
    ms    = (time.perf_counter() - start) * 1000

    sys.stdout.write(" ".join(str(-1 if d == INF else d) for d in dist) + "\n")
    sys.stderr.write(f"{ms:.3f}\n")

if __name__ == "__main__":
    main()