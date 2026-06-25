use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;

fn partition(arr: &mut [i64], l: usize, r: usize) -> usize {
    let pivot = arr[r];
    let mut i = l;
    for j in l..r {
        if arr[j] <= pivot {
            arr.swap(i, j);
            i += 1;
        }
    }
    arr.swap(i, r);
    i
}

fn quicksort(arr: &mut [i64], l: usize, r: usize) {
    if l >= r { return; }
    let p = partition(arr, l, r);
    if p > 0 { quicksort(arr, l, p - 1); }
    quicksort(arr, p + 1, r);
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut iter = input.split_ascii_whitespace();

    let n: usize = iter.next().unwrap().parse().unwrap();
    let mut arr: Vec<i64> = (0..n)
        .map(|_| iter.next().unwrap().parse().unwrap())
        .collect();

    let start = Instant::now();
    if n > 1 { quicksort(&mut arr, 0, n - 1); }
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