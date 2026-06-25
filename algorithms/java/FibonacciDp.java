import java.io.*;

public class FibonacciDp {

    static final long MOD = 1_000_000_007L;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());

        long start = System.nanoTime();

        long[] memo = new long[n + 1];
        if (n > 0) memo[1] = 1;
        for (int i = 2; i <= n; i++)
            memo[i] = (memo[i-1] + memo[i-2]) % MOD;

        double ms = (System.nanoTime() - start) / 1e6;

        PrintWriter pw = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));
        pw.println(memo[n]);
        pw.flush();
        System.err.printf("%.3f%n", ms);
    }
}