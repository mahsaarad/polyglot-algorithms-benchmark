import os
import random
import string
import math

# ساختار پوشه ها
BASE_DIR = "inputs"
ALGORITHMS = [
    "01_mergesort", "02_quicksort", "03_dijkstra", "04_kmp",
    "05_sieve", "06_fft", "07_montecarlo", "08_lcs",
    "09_knapsack", "10_fibonacci", "11_matrix", "12_huffman"
]

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

ensure_dir(BASE_DIR)
for algo in ALGORITHMS:
    ensure_dir(os.path.join(BASE_DIR, algo))

print("Generating input files...")

# 01 & 02: Sort (Merge / Quick)
sort_sizes = [1000, 10000, 100000, 1000000, 5000000]
for size in sort_sizes:
    data = [str(random.randint(-1000000, 1000000)) for _ in range(size)]
    content = f"{size}\n" + " ".join(data) + "\n"
    for algo in ["01_mergesort", "02_quicksort"]:
        with open(f"{BASE_DIR}/{algo}/input_{size}.txt", "w") as f:
            f.write(content)

# 03: Dijkstra (V, E)
dijkstra_sizes = [(500, 2000), (5000, 50000), (20000, 200000)]
for v, e in dijkstra_sizes:
    with open(f"{BASE_DIR}/03_dijkstra/input_{v}_{e}.txt", "w") as f:
        f.write(f"{v} {e}\n")
        # Start node: 0
        f.write("0\n") 
        for _ in range(e):
            u = random.randint(0, v - 1)
            dst = random.randint(0, v - 1)
            w = random.randint(1, 1000)
            f.write(f"{u} {dst} {w}\n")

# 04 & 12: KMP & Huffman (String)
string_sizes = [1000, 10000, 100000, 1000000, 5000000]
chars = string.ascii_letters + " "
for size in string_sizes:
    text = ''.join(random.choices(chars, k=size))
    # For KMP
    with open(f"{BASE_DIR}/04_kmp/input_{size}.txt", "w") as f:
        pattern = text[size//2 : size//2 + min(20, size)] # A pattern from the text
        f.write(f"{text}\n{pattern}\n")
    # For Huffman
    if size <= 1000000:
        with open(f"{BASE_DIR}/12_huffman/input_{size}.txt", "w") as f:
            f.write(f"{text}\n")

# 05: Sieve & 07: Monte Carlo (Just N)
sieve_sizes = [10**6, 10**7, 10**8, 2 * 10**8]
for size in sieve_sizes:
    with open(f"{BASE_DIR}/05_sieve/input_{size}.txt", "w") as f:
        f.write(f"{size}\n")

mc_sizes = [100000, 1000000, 10000000, 50000000]
for size in mc_sizes:
    with open(f"{BASE_DIR}/07_montecarlo/input_{size}.txt", "w") as f:
        f.write(f"{size}\n")

# 06: FFT (N powers of 2)
fft_sizes = [1024, 65536, 524288, 1048576]
for size in fft_sizes:
    with open(f"{BASE_DIR}/06_fft/input_{size}.txt", "w") as f:
        f.write(f"{size}\n")
        for _ in range(size):
            f.write(f"{random.uniform(-10.0, 10.0):.4f} 0.0\n")

# 08: LCS
lcs_sizes = [500, 1000, 2000, 4000]
for size in lcs_sizes:
    s1 = ''.join(random.choices(string.ascii_uppercase, k=size))
    s2 = ''.join(random.choices(string.ascii_uppercase, k=size))
    with open(f"{BASE_DIR}/08_lcs/input_{size}.txt", "w") as f:
        f.write(f"{s1}\n{s2}\n")

# 09: Knapsack (W, n)
knap_sizes = [(1000, 100), (10000, 500), (50000, 1000)]
for w, n in knap_sizes:
    with open(f"{BASE_DIR}/09_knapsack/input_W{w}_n{n}.txt", "w") as f:
        f.write(f"{n} {w}\n")
        for _ in range(n):
            val = random.randint(10, 500)
            wt = random.randint(1, w // 10)
            f.write(f"{val} {wt}\n")

# 10: Fibonacci
fibo_sizes = [40, 10000, 100000, 1000000]
for size in fibo_sizes:
    with open(f"{BASE_DIR}/10_fibonacci/input_{size}.txt", "w") as f:
        f.write(f"{size}\n")

# 11: Matrix Multiplication
matrix_sizes = [64, 128, 256, 512]
for size in matrix_sizes:
    with open(f"{BASE_DIR}/11_matrix/input_{size}.txt", "w") as f:
        f.write(f"{size}\n")
        # Matrix A
        for _ in range(size):
            row = [str(random.randint(1, 10)) for _ in range(size)]
            f.write(" ".join(row) + "\n")
        # Matrix B
        for _ in range(size):
            row = [str(random.randint(1, 10)) for _ in range(size)]
            f.write(" ".join(row) + "\n")

print("All test files generated successfully!")
