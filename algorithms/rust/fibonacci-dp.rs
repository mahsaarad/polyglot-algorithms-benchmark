use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;

const MOD: u64 = 1_000_000_007;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let n: usize = input.trim().parse().unwrap();

    let start = Instant::now();

    let mut memo = vec![0u64; n + 1];
    if n > 0 { memo[1] = 1; }
    for i in 2..=n {
        memo[i] = (memo[i-1] + memo[i-2]) % MOD;
    }

    let ms = start.elapsed().as_secs_f64() * 1000.0;

    let stdout = io::stdout();
    let mut out = BufWriter::new(stdout.lock());
    writeln!(out, "{}", memo[n]).unwrap();
    eprintln!("{:.3}", ms);
}