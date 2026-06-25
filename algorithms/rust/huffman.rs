use std::io::{self, Read, Write, BufWriter};
use std::time::Instant;
use std::collections::BinaryHeap;
use std::cmp::Reverse;

#[derive(Eq, PartialEq)]
enum Node {
    Leaf { freq: usize, ch: u8 },
    Internal { freq: usize, left: Box<Node>, right: Box<Node> },
}

impl Node {
    fn freq(&self) -> usize {
        match self { Node::Leaf{freq,..} | Node::Internal{freq,..} => *freq }
    }
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.freq().cmp(&other.freq())
    }
}
impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

fn build_codes(node: &Node, depth: usize, codes: &mut [usize; 256]) {
    match node {
        Node::Leaf { ch, .. } => {
            codes[*ch as usize] = if depth > 0 { depth } else { 1 };
        }
        Node::Internal { left, right, .. } => {
            build_codes(left,  depth + 1, codes);
            build_codes(right, depth + 1, codes);
        }
    }
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let text = input.trim().as_bytes();
    let len  = text.len();

    let mut freq = [0usize; 256];
    for &b in text { freq[b as usize] += 1; }

    let start = Instant::now();

    let mut heap: BinaryHeap<Reverse<Box<Node>>> = BinaryHeap::new();
    let mut unique = 0;
    for (ch, &f) in freq.iter().enumerate() {
        if f > 0 {
            heap.push(Reverse(Box::new(Node::Leaf { freq: f, ch: ch as u8 })));
            unique += 1;
        }
    }

    while heap.len() > 1 {
        let Reverse(l) = heap.pop().unwrap();
        let Reverse(r) = heap.pop().unwrap();
        let f = l.freq() + r.freq();
        heap.push(Reverse(Box::new(Node::Internal {
            freq: f, left: l, right: r
        })));
    }

    let mut codes = [0usize; 256];
    if let Some(Reverse(root)) = heap.pop() {
        build_codes(&root, 0, &mut codes);
    }

    let total_bits: usize = (0..256)
        .filter(|&i| freq[i] > 0)
        .map(|i| freq[i] * codes[i])
        .sum();

    let ms    = start.elapsed().as_secs_f64() * 1000.0;
    let ratio = total_bits as f64 / (8.0 * len as f64);

    let stdout = io::stdout();
    let mut out = BufWriter::new(stdout.lock());
    writeln!(out, "{}", unique).unwrap();
    writeln!(out, "{}", total_bits).unwrap();
    writeln!(out, "{:.2}", ratio).unwrap();
    eprintln!("{:.3}", ms);
}