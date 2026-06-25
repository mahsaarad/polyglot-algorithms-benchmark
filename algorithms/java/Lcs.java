import java.util.*;
import java.io.*;

public class Lcs {

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String a = br.readLine().trim();
        String b = br.readLine().trim();
        int n = a.length(), m = b.length();

        long start = System.nanoTime();

        int[] prev = new int[m + 1];
        int[] curr = new int[m + 1];

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                if (a.charAt(i-1) == b.charAt(j-1))
                    curr[j] = prev[j-1] + 1;
                else
                    curr[j] = Math.max(curr[j-1], prev[j]);
            }
            int[] tmp = prev; prev = curr; curr = tmp;
            Arrays.fill(curr, 0);
        }

        double ms = (System.nanoTime() - start) / 1e6;

        PrintWriter pw = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));
        pw.println(prev[m]);
        pw.flush();
        System.err.printf("%.3f%n", ms);
    }
}