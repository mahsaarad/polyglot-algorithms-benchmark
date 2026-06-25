import java.util.*;
import java.io.*;

public class Matrix {

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());

        long[][] A = new long[n][n];
        long[][] B = new long[n][n];
        long[][] C = new long[n][n];

        for (int i = 0; i < n; i++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            for (int j = 0; j < n; j++)
                A[i][j] = Long.parseLong(st.nextToken());
        }
        for (int i = 0; i < n; i++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            for (int j = 0; j < n; j++)
                B[i][j] = Long.parseLong(st.nextToken());
        }

        long start = System.nanoTime();

        for (int i = 0; i < n; i++)
            for (int k = 0; k < n; k++) {
                long aik = A[i][k];
                for (int j = 0; j < n; j++)
                    C[i][j] += aik * B[k][j];
            }

        double ms = (System.nanoTime() - start) / 1e6;

        long checksum = 0;
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                checksum += C[i][j];

        PrintWriter pw = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));
        pw.println(checksum);
        pw.flush();
        System.err.printf("%.3f%n", ms);
    }
}