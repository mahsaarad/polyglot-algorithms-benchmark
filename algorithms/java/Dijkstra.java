import java.util.*;
import java.io.*;

public class Dijkstra {

    static final int INF = Integer.MAX_VALUE / 2;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int V   = Integer.parseInt(st.nextToken());
        int E   = Integer.parseInt(st.nextToken());
        int src = Integer.parseInt(st.nextToken());

        List<int[]>[] graph = new ArrayList[V];
        for (int i = 0; i < V; i++) graph[i] = new ArrayList<>();

        for (int i = 0; i < E; i++) {
            st = new StringTokenizer(br.readLine());
            int u = Integer.parseInt(st.nextToken());
            int t = Integer.parseInt(st.nextToken());
            int w = Integer.parseInt(st.nextToken());
            graph[u].add(new int[]{t, w});
        }

        long start = System.nanoTime();

        int[] dist = new int[V];
        Arrays.fill(dist, INF);
        dist[src] = 0;

        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));
        pq.offer(new int[]{0, src});

        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int d = cur[0], u = cur[1];
            if (d > dist[u]) continue;
            for (int[] e : graph[u]) {
                int nd = d + e[1];
                if (nd < dist[e[0]]) {
                    dist[e[0]] = nd;
                    pq.offer(new int[]{nd, e[0]});
                }
            }
        }

        double ms = (System.nanoTime() - start) / 1e6;

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < V; i++) {
            if (i > 0) sb.append(' ');
            sb.append(dist[i] == INF ? -1 : dist[i]);
        }
        System.out.println(sb);
        System.err.printf("%.3f%n", ms);
    }
}