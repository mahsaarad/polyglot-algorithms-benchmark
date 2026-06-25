use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut iter = input.split_ascii_whitespace();

    let n: usize = iter.next().unwrap().parse().unwrap();
    let size = n * n;

    let a: Vec<i64> = (0..size)
        .map(|_| iter.next().unwrap().parse().unwrap())
        .collect();
    let b: Vec<i64> = (0..size)
        .map(|_| iter.next().unwrap().parse().unwrap())
        .collect();
    let mut c = vec![0i64; size];

    let start = Instant::now();

    for i in 0..n {
        for k in 0..n {
            let aik = a[i*n + k];
            for j in 0..n {
                c[i*n + j] += aik * b[k*n + j];
            }
        }
    }

    let ms = start.elapsed().as_secs_f64() * 1000.0;

    let checksum: i64 = c.iter().sum();
    let stdout = io::stdout();
    let mut out = BufWriter::new(stdout.lock());
    writeln!(out, "{}", checksum).unwrap();
    eprintln!("{:.3}", ms);
}