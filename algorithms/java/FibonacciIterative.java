import java.io.*;

public class FibonacciIterative {

    static final long MOD = 1_000_000_007L;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());

        long start = System.nanoTime();

        long result;
        if (n == 0) {
            result = 0;
        } else {
            long a = 0, b = 1;
            for (long i = 2; i <= n; i++) {
                long c = (a + b) % MOD;
                a = b; b = c;
            }
            result = b;
        }

        double ms = (System.nanoTime() - start) / 1e6;

        PrintWriter pw = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));
        pw.println(result);
        pw.flush();
        System.err.printf("%.3f%n", ms);
    }
}