import java.util.*;
import java.io.*;

public class Sieve {

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());

        long start = System.nanoTime();

        boolean[] isComposite = new boolean[n + 1];
        isComposite[0] = true;
        if (n > 0) isComposite[1] = true;

        for (int i = 2; (long) i * i <= n; i++) {
            if (!isComposite[i]) {
                for (int j = i * i; j <= n; j += i)
                    isComposite[j] = true;
            }
        }

        long count = 0, last = -1;
        for (int k = 2; k <= n; k++) {
            if (!isComposite[k]) { count++; last = k; }
        }

        double ms = (System.nanoTime() - start) / 1e6;

        PrintWriter pw = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));
        pw.println(count);
        pw.println(last);
        pw.flush();
        System.err.printf("%.3f%n", ms);
    }
}