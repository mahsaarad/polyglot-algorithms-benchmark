import java.util.*;
import java.io.*;

public class Montecarlo {

    static long seed;

    static double lcgNext() {
        seed = (seed * 1664525L + 1013904223L) & 0xFFFFFFFFL;
        return (seed >> 1) / (double)(1L << 31);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n    = Long.parseLong(br.readLine().trim());
        seed      = Long.parseUnsignedLong(br.readLine().trim());

        long start  = System.nanoTime();

        long inside = 0;
        for (long i = 0; i < n; i++) {
            double x = lcgNext();
            double y = lcgNext();
            if (x*x + y*y <= 1.0) inside++;
        }
        double pi = 4.0 * inside / n;

        double ms = (System.nanoTime() - start) / 1e6;

        PrintWriter pw = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));
        pw.printf("%.8f%n", pi);
        pw.flush();
        System.err.printf("%.3f%n", ms);
    }
}