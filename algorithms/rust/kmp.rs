use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;

fn build_lps(pat: &[u8]) -> Vec<usize> {
    let m = pat.len();
    let mut lps = vec![0usize; m];
    let mut len = 0usize;
    let mut i   = 1;
    while i < m {
        if pat[i] == pat[len] {
            len += 1;
            lps[i] = len;
            i += 1;
        } else if len > 0 {
            len = lps[len - 1];
        } else {
            lps[i] = 0;
            i += 1;
        }
    }
    lps
}

fn kmp(text: &[u8], pat: &[u8]) -> Vec<usize> {
    let (n, m) = (text.len(), pat.len());
    if m == 0 { return vec![]; }
    let lps  = build_lps(pat);
    let mut matches = Vec::new();
    let (mut i, mut j) = (0, 0);
    while i < n {
        if text[i] == pat[j] { i += 1; j += 1; }
        if j == m {
            matches.push(i - j);
            j = lps[j - 1];
        } else if i < n && text[i] != pat[j] {
            if j > 0 { j = lps[j - 1]; } else { i += 1; }
        }
    }
    matches
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();
    let text = lines.next().unwrap_or("").trim().as_bytes().to_vec();
    let pat  = lines.next().unwrap_or("").trim().as_bytes().to_vec();

    let start   = Instant::now();
    let matches = kmp(&text, &pat);
    let ms      = start.elapsed().as_secs_f64() * 1000.0;

    let stdout = io::stdout();
    let mut out = BufWriter::new(stdout.lock());
    writeln!(out, "{}", matches.len()).unwrap();
    if matches.is_empty() {
        writeln!(out).unwrap();
    } else {
        let s: Vec<String> = matches.iter().map(|x| x.to_string()).collect();
        writeln!(out, "{}", s.join(" ")).unwrap();
    }
    eprintln!("{:.3}", ms);
}