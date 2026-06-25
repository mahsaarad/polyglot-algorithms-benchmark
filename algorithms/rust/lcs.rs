use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();

    let a: Vec<u8> = lines.next().unwrap_or("").trim().as_bytes().to_vec();
    let b: Vec<u8> = lines.next().unwrap_or("").trim().as_bytes().to_vec();
    let (n, m)     = (a.len(), b.len());

    let start = Instant::now();

    let mut prev = vec![0usize; m + 1];
    let mut curr = vec![0usize; m + 1];

    for i in 1..=n {
        for j in 1..=m {
            curr[j] = if a[i-1] == b[j-1] {
                prev[j-1] + 1
            } else {
                curr[j-1].max(prev[j])
            };
        }
        std::mem::swap(&mut prev, &mut curr);
        curr.iter_mut().for_each(|x| *x = 0);
    }

    let ms = start.elapsed().as_secs_f64() * 1000.0;

    let stdout = io::stdout();
    let mut out = BufWriter::new(stdout.lock());
    writeln!(out, "{}", prev[m]).unwrap();
    eprintln!("{:.3}", ms);
}