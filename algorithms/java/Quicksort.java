import java.util.*;
import java.io.*;

public class Quicksort {

    static int partition(int[] arr, int l, int r) {
        int pivot = arr[r], i = l;
        for (int j = l; j < r; j++) {
            if (arr[j] <= pivot) {
                int t = arr[i]; arr[i] = arr[j]; arr[j] = t;
                i++;
            }
        }
        int t = arr[i]; arr[i] = arr[r]; arr[r] = t;
        return i;
    }

    static void quicksort(int[] arr, int l, int r) {
        if (l >= r) return;
        int p = partition(arr, l, r);
        quicksort(arr, l, p - 1);
        quicksort(arr, p + 1, r);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] arr = new int[n];
        for (int i = 0; i < n; i++)
            arr[i] = Integer.parseInt(st.nextToken());

        long start = System.nanoTime();
        quicksort(arr, 0, n - 1);
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