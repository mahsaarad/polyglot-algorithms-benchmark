#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define INF 1000000000

typedef struct { int to, w, next; } Edge;
typedef struct { int dist, node; } HeapNode;

Edge *edges;
int  *head, ecnt;

void add_edge(int u, int v, int w) {
    edges[ecnt] = (Edge){v, w, head[u]};
    head[u] = ecnt++;
}

HeapNode heap[4000000];
int heap_sz;

void push(int dist, int node) {
    int i = ++heap_sz;
    heap[i] = (HeapNode){dist, node};
    while (i > 1 && heap[i].dist < heap[i/2].dist) {
        HeapNode t = heap[i]; heap[i] = heap[i/2]; heap[i/2] = t;
        i /= 2;
    }
}

HeapNode pop() {
    HeapNode top = heap[1];
    heap[1] = heap[heap_sz--];
    int i = 1;
    while (1) {
        int s = i, l = 2*i, r = 2*i+1;
        if (l <= heap_sz && heap[l].dist < heap[s].dist) s = l;
        if (r <= heap_sz && heap[r].dist < heap[s].dist) s = r;
        if (s == i) break;
        HeapNode t = heap[i]; heap[i] = heap[s]; heap[s] = t;
        i = s;
    }
    return top;
}

int main() {
    int V, E, src;
    scanf("%d %d %d", &V, &E, &src);

    edges = malloc(E * sizeof(Edge));
    head  = malloc(V * sizeof(int));
    int *dist = malloc(V * sizeof(int));
    int *vis  = calloc(V, sizeof(int));
    for (int i = 0; i < V; i++) { head[i] = -1; dist[i] = INF; }

    for (int i = 0; i < E; i++) {
        int u, v, w; scanf("%d %d %d", &u, &v, &w);
        add_edge(u, v, w);
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    dist[src] = 0;
    push(0, src);
    while (heap_sz > 0) {
        HeapNode cur = pop();
        if (vis[cur.node]) continue;
        vis[cur.node] = 1;
        for (int e = head[cur.node]; e != -1; e = edges[e].next) {
            int to = edges[e].to, nd = cur.dist + edges[e].w;
            if (nd < dist[to]) { dist[to] = nd; push(nd, to); }
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double ms = (end.tv_sec  - start.tv_sec)  * 1000.0
              + (end.tv_nsec - start.tv_nsec) / 1e6;

    for (int i = 0; i < V; i++)
        printf("%d%c", dist[i] == INF ? -1 : dist[i], i < V-1 ? ' ' : '\n');
    fprintf(stderr, "%.3f\n", ms);

    free(edges); free(head); free(dist); free(vis);
    return 0;
}