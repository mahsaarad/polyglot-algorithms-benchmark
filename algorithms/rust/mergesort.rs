use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;

fn merge(arr: &mut [i64], tmp: &mut [i64], l: usize, m: usize, r: usize) {
    tmp[l..=r].copy_from_slice(&arr[l..=r]);
    let (mut i, mut j, mut k) = (l, m + 1, l);
    while i <= m && j <= r {
        if tmp[i] <= tmp[j] { arr[k] = tmp[i]; i += 1; }
        else                 { arr[k] = tmp[j]; j += 1; }
        k += 1;
    }
    while i <= m { arr[k] = tmp[i]; i += 1; k += 1; }
    while j <= r { arr[k] = tmp[j]; j += 1; k += 1; }
}

fn mergesort(arr: &mut [i64], tmp: &mut [i64], l: usize, r: usize) {
    if l >= r { return; }
    let m = l + (r - l) / 2;
    mergesort(arr, tmp, l, m);
    mergesort(arr, tmp, m + 1, r);
    merge(arr, tmp, l, m, r);
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut iter = input.split_ascii_whitespace();

    let n: usize = iter.next().unwrap().parse().unwrap();
    let mut arr: Vec<i64> = (0..n)
        .map(|_| iter.next().unwrap().parse().unwrap())
        .collect();
    let mut tmp = vec![0i64; n];

    let start = Instant::now();
    if n > 1 { mergesort(&mut arr, &mut tmp, 0, n - 1); }
    let ms = start.elapsed().as_secs_f64() * 1000.0;

    let stdout = io::stdout();
    let mut out = BufWriter::new(stdout.lock());
    for (i, v) in arr.iter().enumerate() {
        if i > 0 { write!(out, " ").unwrap(); }
        write!(out, "{}", v).unwrap();
    }
    writeln!(out).unwrap();
    eprintln!("{:.3}", ms);
}