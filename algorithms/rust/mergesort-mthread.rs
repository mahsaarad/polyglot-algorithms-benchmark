use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;
use std::thread;

fn merge_vecs(left: &[i64], right: &[i64]) -> Vec<i64> {
    let mut result = Vec::with_capacity(left.len() + right.len());
    let (mut i, mut j) = (0, 0);
    while i < left.len() && j < right.len() {
        if left[i] <= right[j] { result.push(left[i]); i += 1; }
        else                   { result.push(right[j]); j += 1; }
    }
    result.extend_from_slice(&left[i..]);
    result.extend_from_slice(&right[j..]);
    result
}

fn mergesort(arr: Vec<i64>) -> Vec<i64> {
    if arr.len() <= 1 { return arr; }
    let mid = arr.len() / 2;
    let right = arr[mid..].to_vec();
    let mut left = arr;
    left.truncate(mid);
    let left  = mergesort(left);
    let right = mergesort(right);
    merge_vecs(&left, &right)
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut iter = input.split_ascii_whitespace();

    let n: usize = iter.next().unwrap().parse().unwrap();
    let arr: Vec<i64> = (0..n)
        .map(|_| iter.next().unwrap().parse().unwrap())
        .collect();

    let num_threads = 4usize;
    let chunk_size  = (n + num_threads - 1) / num_threads;

    let start = Instant::now();

    // هر chunk در یک thread مستقل sort می‌شه
    let sorted_chunks: Vec<Vec<i64>> = thread::scope(|s| {
        arr.chunks(chunk_size)
            .map(|chunk| {
                let c = chunk.to_vec();
                s.spawn(|| mergesort(c))
            })
            .collect::<Vec<_>>()
            .into_iter()
            .map(|h| h.join().unwrap())
            .collect()
    });

    // merge نهایی
    let result = sorted_chunks
        .into_iter()
        .reduce(|a, b| merge_vecs(&a, &b))
        .unwrap_or_default();

    let ms = start.elapsed().as_secs_f64() * 1000.0;

    let stdout = io::stdout();
    let mut out = BufWriter::new(stdout.lock());
    for (i, v) in result.iter().enumerate() {
        if i > 0 { write!(out, " ").unwrap(); }
        write!(out, "{}", v).unwrap();
    }
    writeln!(out).unwrap();
    eprintln!("{:.3}", ms);
}