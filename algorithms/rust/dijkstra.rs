use std::collections::BinaryHeap;
use std::cmp::Reverse;
use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;

const INF: i64 = 1_000_000_000;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut iter = input.split_ascii_whitespace();

    let v: usize = iter.next().unwrap().parse().unwrap();
    let e: usize = iter.next().unwrap().parse().unwrap();
    let src: usize = iter.next().unwrap().parse().unwrap();

    let mut graph: Vec<Vec<(usize, i64)>> = vec![vec![]; v];
    for _ in 0..e {
        let u: usize = iter.next().unwrap().parse().unwrap();
        let to: usize = iter.next().unwrap().parse().unwrap();
        let w: i64   = iter.next().unwrap().parse().unwrap();
        graph[u].push((to, w));
    }

    let start = Instant::now();

    let mut dist = vec![INF; v];
    dist[src] = 0;
    let mut heap = BinaryHeap::new();
    heap.push(Reverse((0i64, src)));

    while let Some(Reverse((d, u))) = heap.pop() {
        if d > dist[u] { continue; }
        for &(to, w) in &graph[u] {
            let nd = d + w;
            if nd < dist[to] {
                dist[to] = nd;
                heap.push(Reverse((nd, to)));
            }
        }
    }

    let ms = start.elapsed().as_secs_f64() * 1000.0;

    let stdout = io::stdout();
    let mut out = BufWriter::new(stdout.lock());
    for (i, &d) in dist.iter().enumerate() {
        if i > 0 { write!(out, " ").unwrap(); }
        write!(out, "{}", if d == INF { -1 } else { d }).unwrap();
    }
    writeln!(out).unwrap();
    eprintln!("{:.3}", ms);
}