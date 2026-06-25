use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;

const MOD: u64 = 1_000_000_007;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let n: u64 = input.trim().parse().unwrap();

    let start = Instant::now();

    let result = if n == 0 {
        0
    } else {
        let (mut a, mut b) = (0u64, 1u64);
        for _ in 2..=n {
            let c = (a + b) % MOD;
            a = b; b = c;
        }
        b
    };

    let ms = start.elapsed().as_secs_f64() * 1000.0;

    let stdout = io::stdout();
    let mut out = BufWriter::new(stdout.lock());
    writeln!(out, "{}", result).unwrap();
    eprintln!("{:.3}", ms);
}