use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;
use std::f64::consts::PI;

#[derive(Clone, Copy)]
struct Complex { r: f64, i: f64 }

impl Complex {
    fn new(r: f64, i: f64) -> Self { Complex { r, i } }
    fn add(self, o: Self) -> Self { Complex::new(self.r + o.r, self.i + o.i) }
    fn sub(self, o: Self) -> Self { Complex::new(self.r - o.r, self.i - o.i) }
    fn mul(self, o: Self) -> Self {
        Complex::new(self.r*o.r - self.i*o.i,
                     self.r*o.i + self.i*o.r)
    }
    fn abs(self) -> f64 { (self.r*self.r + self.i*self.i).sqrt() }
}

fn fft(a: &mut Vec<Complex>) {
    let n = a.len();
    // bit-reversal
    let mut j = 0usize;
    for i in 1..n {
        let mut bit = n >> 1;
        while j & bit != 0 { j ^= bit; bit >>= 1; }
        j ^= bit;
        if i < j { a.swap(i, j); }
    }
    // butterfly
    let mut len = 2;
    while len <= n {
        let ang  = 2.0 * PI / len as f64;
        let wlen = Complex::new(ang.cos(), ang.sin());
        let mut i = 0;
        while i < n {
            let mut w = Complex::new(1.0, 0.0);
            for jj in 0..len/2 {
                let u = a[i + jj];
                let v = a[i + jj + len/2].mul(w);
                a[i + jj]        = u.add(v);
                a[i + jj + len/2] = u.sub(v);
                w = w.mul(wlen);
            }
            i += len;
        }
        len <<= 1;
    }
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut iter = input.split_ascii_whitespace();

    let n: usize = iter.next().unwrap().parse().unwrap();
    let mut a: Vec<Complex> = (0..n)
        .map(|_| Complex::new(iter.next().unwrap().parse().unwrap(), 0.0))
        .collect();

    let start = Instant::now();
    fft(&mut a);
    let ms = start.elapsed().as_secs_f64() * 1000.0;

    let k   = n.min(5);
    let sum: f64 = a[..k].iter().map(|c| c.abs()).sum();

    let stdout = io::stdout();
    let mut out = BufWriter::new(stdout.lock());
    writeln!(out, "{:.6}", sum).unwrap();
    eprintln!("{:.3}", ms);
}