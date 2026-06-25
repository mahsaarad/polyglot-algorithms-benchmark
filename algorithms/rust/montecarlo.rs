use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;

fn lcg_next(s: &mut u32) -> f64 {
    *s = s.wrapping_mul(1_664_525).wrapping_add(1_013_904_223);
    (*s >> 1) as f64 / (1u32 << 31) as f64
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut iter = input.split_ascii_whitespace();

    let n:    u64 = iter.next().unwrap().parse().unwrap();
    let seed: u32 = iter.next().unwrap().parse().unwrap();

    let start = Instant::now();

    let mut s      = seed;
    let mut inside = 0u64;
    for _ in 0..n {
        let x = lcg_next(&mut s);
        let y = lcg_next(&mut s);
        if x*x + y*y <= 1.0 { inside += 1; }
    }
    let pi = 4.0 * inside as f64 / n as f64;

    let ms = start.elapsed().as_secs_f64() * 1000.0;

    let stdout = io::stdout();
    let mut out = BufWriter::new(stdout.lock());
    writeln!(out, "{:.8}", pi).unwrap();
    eprintln!("{:.3}", ms);
}