use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let n: usize = input.trim().parse().unwrap();

    let start = Instant::now();

    let mut is_composite = vec![false; n + 1];
    is_composite[0] = true;
    if n > 0 { is_composite[1] = true; }

    let mut i = 2;
    while i * i <= n {
        if !is_composite[i] {
            let mut j = i * i;
            while j <= n {
                is_composite[j] = true;
                j += i;
            }
        }
        i += 1;
    }

    let mut count = 0u64;
    let mut last  = 0i64;
    for k in 2..=n {
        if !is_composite[k] {
            count += 1;
            last   = k as i64;
        }
    }

    let ms = start.elapsed().as_secs_f64() * 1000.0;

    let stdout = io::stdout();
    let mut out = BufWriter::new(stdout.lock());
    writeln!(out, "{}", count).unwrap();
    writeln!(out, "{}", last).unwrap();
    eprintln!("{:.3}", ms);
}