use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;
use std::thread;
use std::sync::Arc;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut iter = input.split_ascii_whitespace();

    let n: usize = iter.next().unwrap().parse().unwrap();
    let size = n * n;

    let a: Arc<Vec<i64>> = Arc::new(
        (0..size).map(|_| iter.next().unwrap().parse().unwrap()).collect()
    );
    let b: Arc<Vec<i64>> = Arc::new(
        (0..size).map(|_| iter.next().unwrap().parse().unwrap()).collect()
    );

    let num_threads = 4;
    let chunk       = (n + num_threads - 1) / num_threads;

    let start = Instant::now();

    let handles: Vec<_> = (0..num_threads).map(|t| {
        let a   = Arc::clone(&a);
        let b   = Arc::clone(&b);
        let row_start = t * chunk;
        let row_end   = ((t+1)*chunk).min(n);

        thread::spawn(move || {
            let mut local = vec![0i64; (row_end - row_start) * n];
            for i in row_start..row_end {
                for k in 0..n {
                    let aik = a[i*n + k];
                    for j in 0..n {
                        local[(i-row_start)*n + j] += aik * b[k*n + j];
                    }
                }
            }
            (row_start, local)
        })
    }).collect();

    let mut c = vec![0i64; size];
    for h in handles {
        let (row_start, local) = h.join().unwrap();
        let rows = local.len() / n;
        for i in 0..rows {
            for j in 0..n {
                c[(row_start+i)*n + j] = local[i*n + j];
            }
        }
    }

    let ms = start.elapsed().as_secs_f64() * 1000.0;

    let checksum: i64 = c.iter().sum();
    let stdout = io::stdout();
    let mut out = BufWriter::new(stdout.lock());
    writeln!(out, "{}", checksum).unwrap();
    eprintln!("{:.3}", ms);
}