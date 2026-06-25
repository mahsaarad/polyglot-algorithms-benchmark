use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;

const MOD: u64 = 1_000_000_007;

fn fib(n: u32) -> u64 {
    if n <= 1 { return n as u64; }
    (fib(n-1) + fib(n-2)) % MOD
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let n: u32 = input.trim().parse().unwrap();

    let start  = Instant::now();
    let result = fib(n);
    let ms     = start.elapsed().as_secs_f64() * 1000.0;

    let stdout = io::stdout();
    let mut out = BufWriter::new(stdout.lock());
    writeln!(out, "{}", result).unwrap();
    eprintln!("{:.3}", ms);
}