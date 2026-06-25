import java.util.*;
import java.io.*;

public class Mergesort {

    private static int[] tmp;

    static void merge(int[] arr, int l, int m, int r) {
        System.arraycopy(arr, l, tmp, l, r - l + 1);
        int i = l, j = m + 1, k = l;
        while (i <= m && j <= r)
            arr[k++] = tmp[i] <= tmp[j] ? tmp[i++] : tmp[j++];
        while (i <= m) arr[k++] = tmp[i++];
        while (j <= r) arr[k++] = tmp[j++];
    }

    static void mergesort(int[] arr, int l, int r) {
        if (l >= r) return;
        int m = l + (r - l) / 2;
        mergesort(arr, l, m);
        mergesort(arr, m + 1, r);
        merge(arr, l, m, r);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] arr = new int[n];
        for (int i = 0; i < n; i++)
            arr[i] = Integer.parseInt(st.nextToken());
        tmp = new int[n];

        long start = System.nanoTime();
        mergesort(arr, 0, n - 1);
        double ms = (System.nanoTime() - start) / 1e6;

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            if (i > 0) sb.append(' ');
            sb.append(arr[i]);
        }
        System.out.println(sb);
        System.err.printf("%.3f%n", ms);
    }
}