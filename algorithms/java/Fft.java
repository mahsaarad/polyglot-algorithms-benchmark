import java.util.*;
import java.io.*;

public class Fft {

    static double[] re, im;

    static void fft(int n) {
        // bit-reversal
        for (int i = 1, j = 0; i < n; i++) {
            int bit = n >> 1;
            for (; (j & bit) != 0; bit >>= 1) j ^= bit;
            j ^= bit;
            if (i < j) {
                double t; 
                t = re[i]; re[i] = re[j]; re[j] = t;
                t = im[i]; im[i] = im[j]; im[j] = t;
            }
        }
        // butterfly
        for (int len = 2; len <= n; len <<= 1) {
            double ang  = 2.0 * Math.PI / len;
            double wRe  = Math.cos(ang);
            double wIm  = Math.sin(ang);
            for (int i = 0; i < n; i += len) {
                double curRe = 1.0, curIm = 0.0;
                for (int j = 0; j < len / 2; j++) {
                    double uRe = re[i+j],       uIm = im[i+j];
                    double vRe = re[i+j+len/2], vIm = im[i+j+len/2];
                    double tvRe = vRe*curRe - vIm*curIm;
                    double tvIm = vRe*curIm + vIm*curRe;
                    re[i+j]        = uRe + tvRe;
                    im[i+j]        = uIm + tvIm;
                    re[i+j+len/2]  = uRe - tvRe;
                    im[i+j+len/2]  = uIm - tvIm;
                    double newRe = curRe*wRe - curIm*wIm;
                    curIm = curRe*wIm + curIm*wRe;
                    curRe = newRe;
                }
            }
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br  = new BufferedReader(new InputStreamReader(System.in));
        int n              = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        re = new double[n];
        im = new double[n];
        for (int i = 0; i < n; i++)
            re[i] = Double.parseDouble(st.nextToken());

        long start = System.nanoTime();
        fft(n);
        double ms = (System.nanoTime() - start) / 1e6;

        int k = Math.min(5, n);
        double sum = 0;
        for (int i = 0; i < k; i++)
            sum += Math.sqrt(re[i]*re[i] + im[i]*im[i]);

        PrintWriter pw = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));
        pw.printf("%.6f%n", sum);
        pw.flush();
        System.err.printf("%.3f%n", ms);
    }
}