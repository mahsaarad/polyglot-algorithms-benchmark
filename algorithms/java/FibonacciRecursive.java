import java.io.*;

public class FibonacciRecursive {

    static final long MOD = 1_000_000_007L;

    static long fib(int n) {
        if (n <= 1) return n;
        return (fib(n-1) + fib(n-2)) % MOD;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());

        long start  = System.nanoTime();
        long result = fib(n);
        double ms   = (System.nanoTime() - start) / 1e6;

        PrintWriter pw = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));
        pw.println(result);
        pw.flush();
        System.err.printf("%.3f%n", ms);
    }
}