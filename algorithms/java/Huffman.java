import java.util.*;
import java.io.*;

public class Huffman {

    static class Node implements Comparable<Node> {
        int  freq;
        byte ch;
        Node left, right;
        Node(int f, byte c)           { freq=f; ch=c; }
        Node(int f, Node l, Node r)   { freq=f; left=l; right=r; }
        public int compareTo(Node o)  { return Integer.compare(freq, o.freq); }
    }

    static int[] codeLens = new int[256];

    static void buildCodes(Node n, int depth) {
        if (n == null) return;
        if (n.left == null && n.right == null) {
            codeLens[n.ch & 0xFF] = depth > 0 ? depth : 1;
            return;
        }
        buildCodes(n.left,  depth+1);
        buildCodes(n.right, depth+1);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br   = new BufferedReader(new InputStreamReader(System.in));
        String         text = br.readLine().trim();
        int            n    = text.length();

        int[] freq = new int[256];
        for (char c : text.toCharArray()) freq[c]++;

        long start = System.nanoTime();

        PriorityQueue<Node> pq = new PriorityQueue<>();
        int unique = 0;
        for (int i = 0; i < 256; i++) {
            if (freq[i] > 0) {
                pq.offer(new Node(freq[i], (byte)i));
                unique++;
            }
        }

        while (pq.size() > 1) {
            Node l = pq.poll(), r = pq.poll();
            pq.offer(new Node(l.freq + r.freq, l, r));
        }

        if (!pq.isEmpty()) buildCodes(pq.poll(), 0);

        long totalBits = 0;
        for (int i = 0; i < 256; i++)
            if (freq[i] > 0) totalBits += (long)freq[i] * codeLens[i];

        double ms    = (System.nanoTime() - start) / 1e6;
        double ratio = (double)totalBits / (8.0 * n);

        PrintWriter pw = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));
        pw.println(unique);
        pw.println(totalBits);
        pw.printf("%.2f%n", ratio);
        pw.flush();
        System.err.printf("%.3f%n", ms);
    }
}