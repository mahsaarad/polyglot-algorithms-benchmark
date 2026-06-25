import java.util.*;
import java.io.*;

public class Knapsack {

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int W = Integer.parseInt(st.nextToken());
        int n = Integer.parseInt(st.nextToken());

        int[] weight = new int[n];
        int[] value  = new int[n];
        for (int i = 0; i < n; i++) {
            st = new StringTokenizer(br.readLine());
            weight[i] = Integer.parseInt(st.nextToken());
            value[i]  = Integer.parseInt(st.nextToken());
        }

        long start = System.nanoTime();

        int[] dp = new int[W + 1];
        for (int i = 0; i < n; i++)
            for (int w = W; w >= weight[i]; w--) {
                int v = dp[w - weight[i]] + value[i];
                if (v > dp[w]) dp[w] = v;
            }

        double ms = (System.nanoTime() - start) / 1e6;

        PrintWriter pw = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));
        pw.println(dp[W]);
        pw.flush();
        System.err.printf("%.3f%n", ms);
    }
}