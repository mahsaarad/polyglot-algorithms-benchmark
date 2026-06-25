import java.util.*;
import java.io.*;

public class Kmp {

    static int[] buildLPS(String pat) {
        int m   = pat.length();
        int[] lps = new int[m];
        int len = 0, i = 1;
        while (i < m) {
            if (pat.charAt(i) == pat.charAt(len)) {
                lps[i++] = ++len;
            } else if (len > 0) {
                len = lps[len - 1];
            } else {
                lps[i++] = 0;
            }
        }
        return lps;
    }

    static List<Integer> kmp(String text, String pat) {
        int n = text.length(), m = pat.length();
        List<Integer> matches = new ArrayList<>();
        if (m == 0) return matches;
        int[] lps = buildLPS(pat);
        int i = 0, j = 0;
        while (i < n) {
            if (text.charAt(i) == pat.charAt(j)) { i++; j++; }
            if (j == m) {
                matches.add(i - j);
                j = lps[j - 1];
            } else if (i < n && text.charAt(i) != pat.charAt(j)) {
                if (j > 0) j = lps[j - 1]; else i++;
            }
        }
        return matches;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String text = br.readLine().trim();
        String pat  = br.readLine().trim();

        long start   = System.nanoTime();
        List<Integer> matches = kmp(text, pat);
        double ms    = (System.nanoTime() - start) / 1e6;

        StringBuilder sb = new StringBuilder();
        sb.append(matches.size()).append('\n');
        if (matches.isEmpty()) {
            sb.append('\n');
        } else {
            for (int k = 0; k < matches.size(); k++) {
                if (k > 0) sb.append(' ');
                sb.append(matches.get(k));
            }
            sb.append('\n');
        }
        System.out.print(sb);
        System.err.printf("%.3f%n", ms);
    }
}