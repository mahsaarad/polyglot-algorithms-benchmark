use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut iter = input.split_ascii_whitespace();

    let w_cap: usize = iter.next().unwrap().parse().unwrap();
    let n:     usize = iter.next().unwrap().parse().unwrap();

    let mut weight = Vec::with_capacity(n);
    let mut value  = Vec::with_capacity(n);
    for _ in 0..n {
        let wi: usize = iter.next().unwrap().parse().unwrap();
        let vi: i64   = iter.next().unwrap().parse().unwrap();
        weight.push(wi);
        value.push(vi);
    }

    let start = Instant::now();

    let mut dp = vec![0i64; w_cap + 1];
    for i in 0..n {
        for w in (weight[i]..=w_cap).rev() {
            let candidate = dp[w - weight[i]] + value[i];
            if candidate > dp[w] { dp[w] = candidate; }
        }
    }

    let ms = start.elapsed().as_secs_f64() * 1000.0;

    let stdout = io::stdout();
    let mut out = BufWriter::new(stdout.lock());
    writeln!(out, "{}", dp[w_cap]).unwrap();
    eprintln!("{:.3}", ms);
}