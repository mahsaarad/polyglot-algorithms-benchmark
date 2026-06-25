#!/usr/bin/env python3
"""
Benchmark Runner — Programming Language Comparison
12 algorithms × 8 languages × (warmup + measured runs)
Metrics: wall time, internal time, RAM, CPU
Output: results/benchmark_TIMESTAMP.csv
"""

import subprocess
import os
import sys
import time
import csv
import random
import string
import struct
import threading
import statistics
from pathlib import Path
from datetime import datetime

try:
    import psutil
except ImportError:
    print("psutil نصب نیست. اجرا کن: pip install psutil")
    sys.exit(1)

# ══════════════════════════════════════════════
#  PATHS
# ══════════════════════════════════════════════
ROOT        = Path(__file__).resolve().parent.parent
ALGO_DIR    = ROOT / "algorithms"
BUILD_DEBUG = ROOT / "builds" / "debug"
BUILD_REL   = ROOT / "builds" / "release"
RESULTS_DIR = ROOT / "results"

for d in [BUILD_DEBUG, BUILD_REL, RESULTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ══════════════════════════════════════════════
#  BENCHMARK CONFIG
# ══════════════════════════════════════════════
TIMEOUT      = 30      # seconds — اگر از این بیشتر شد TIMEOUT ثبت می‌شه
TOTAL_RUNS   = 10      # کل اجراها
WARMUP_RUNS  = 1       # اولی warmup، دور انداخته می‌شه
SLEEP_BETWEEN= 0.5     # ثانیه بین هر run برای خنک شدن CPU

# P-cores فقط — تنظیم بر اساس سیستم
USE_TASKSET  = sys.platform.startswith("linux")
TASKSET_CPUS = "0,1,2,3"   # چهار P-core اول i7 نسل ۱۳

# ══════════════════════════════════════════════
#  INPUT SIZES
# ══════════════════════════════════════════════
SIZES = {
    "mergesort":            [1_000, 10_000, 100_000, 1_000_000, 5_000_000],
    "mergesort-mthread":    [1_000, 10_000, 100_000, 1_000_000, 5_000_000],
    "quicksort":            [1_000, 10_000, 100_000, 1_000_000, 5_000_000],
    "dijkstra":             [(500,2_000),(5_000,50_000),(20_000,200_000)],
    "kmp":                  [10_000, 100_000, 1_000_000, 5_000_000],
    "sieve":                [1_000_000, 10_000_000, 100_000_000, 200_000_000],
    "fft":                  [1_024, 65_536, 524_288, 1_048_576],
    "montecarlo":           [100_000, 1_000_000, 10_000_000, 50_000_000],
    "lcs":                  [500, 1_000, 2_000, 4_000],
    "knapsack":             [(1_000,100),(10_000,500),(50_000,1_000)],
    "fibonacci_recursive":  [30, 35, 38, 40],
    "fibonacci_iterative":  [10_000, 100_000, 1_000_000],
    "fibonacci_dp":         [10_000, 100_000, 1_000_000],
    "matrix":               [64, 128, 256, 512],
    "matrix-mthread":       [64, 128, 256, 512],
    "huffman":              [1_000, 10_000, 100_000, 1_000_000],
}

# سقف ورودی برای زبان‌های کند
CAPS = {
    "python": {
        "sieve":     10_000_000,
        "montecarlo":5_000_000,
        "matrix":    128,
        "matrix-mthread": 128,
        "lcs":       2_000,
        "knapsack":  (10_000, 500),
    },
    "lua": {
        "sieve":     10_000_000,
        "montecarlo":5_000_000,
        "matrix":    128,
        "matrix-mthread": 128,
        "lcs":       2_000,
        "knapsack":  (10_000, 500),
    },
    "haskell": {
        "matrix":    128,
        "matrix-mthread": 128,
        "lcs":       2_000,
    },
}

# ══════════════════════════════════════════════
#  LANGUAGE CONFIG
# ══════════════════════════════════════════════
LANGUAGES = {
    "c": {
        "ext": "c",
        "compile_debug":   "gcc -O0 -pthread {src} -o {out} -lm",
        "compile_release": "gcc -O3 -pthread {src} -o {out} -lm",
        "run":  "{bin}",
        "compiled": True,
    },
    "rust": {
        "ext": "rs",
        "compile_debug":   "rustc {src} -o {out}",
        "compile_release": "rustc -C opt-level=3 {src} -o {out}",
        "run":  "{bin}",
        "compiled": True,
    },
    "go": {
        "ext": "go",
        "compile_debug":   "go build -gcflags='-N -l' -o {out} {src}",
        "compile_release": "go build -o {out} {src}",
        "run":  "{bin}",
        "compiled": True,
    },
    "haskell": {
        "ext": "hs",
        "compile_debug":   "ghc -O0 {src} -o {out}",
        "compile_release": "ghc -O2 {src} -o {out}",
        "run":  "{bin}",
        "compiled": True,
    },
    "java": {
        "ext": "java",
        "compile_debug":   "javac -d {outdir} {src}",
        "compile_release": "javac -d {outdir} {src}",
        "run":  "java -cp {outdir} {classname}",
        "compiled": True,
        "no_opt_flag": True,   # Java JVM همیشه optimize می‌کنه
    },
    "julia": {
        "ext": "jl",
        "compile_debug":   None,
        "compile_release": None,
        "run":  "julia --optimize=0 {src}",
        "run_release": "julia --optimize=3 {src}",
        "compiled": False,
    },
    "lua": {
        "ext": "lua",
        "compile_debug":   None,
        "compile_release": None,
        "run":  "lua {src}",
        "compiled": False,
    },
    "python": {
        "ext": "py",
        "compile_debug":   None,
        "compile_release": None,
        "run":  "python3 {src}",
        "run_release": "python3 -O {src}",
        "compiled": False,
    },
}

# ══════════════════════════════════════════════
#  INPUT GENERATOR
# ══════════════════════════════════════════════
def gen_input(algo: str, size, seed: int = 42) -> str:
    rng = random.Random(seed)

    if algo in ("mergesort", "mergesort-mthread", "quicksort"):
        n = size
        arr = [rng.randint(-(10**9), 10**9) for _ in range(n)]
        return f"{n}\n{' '.join(map(str, arr))}\n"

    if algo == "dijkstra":
        v, e = size
        src  = 0
        edges = set()
        lines = [f"{v} {e} {src}"]
        while len(edges) < e:
            u = rng.randint(0, v-1)
            t = rng.randint(0, v-1)
            if u != t and (u, t) not in edges:
                w = rng.randint(1, 100)
                lines.append(f"{u} {t} {w}")
                edges.add((u, t))
        return "\n".join(lines) + "\n"

    if algo == "kmp":
        n       = size
        pat_len = 10
        chars   = string.ascii_lowercase
        text    = "".join(rng.choices(chars, k=n))
        pat     = "".join(rng.choices(chars[:4], k=pat_len))
        return f"{text}\n{pat}\n"

    if algo == "sieve":
        return f"{size}\n"

    if algo == "fft":
        n    = size
        vals = [round(rng.uniform(-10.0, 10.0), 4) for _ in range(n)]
        return f"{n}\n{' '.join(map(str, vals))}\n"

    if algo == "montecarlo":
        return f"{size}\n42\n"

    if algo == "lcs":
        n    = size
        chars = string.ascii_uppercase
        a    = "".join(rng.choices(chars, k=n))
        b    = "".join(rng.choices(chars, k=n))
        return f"{a}\n{b}\n"

    if algo == "knapsack":
        w_cap, n = size
        lines    = [f"{w_cap} {n}"]
        for _ in range(n):
            w = rng.randint(1, w_cap // 10 or 1)
            v = rng.randint(1, 100)
            lines.append(f"{w} {v}")
        return "\n".join(lines) + "\n"

    if algo == "fibonacci_recursive":
        return f"{size}\n"

    if algo in ("fibonacci_iterative", "fibonacci_dp"):
        return f"{size}\n"

    if algo in ("matrix", "matrix-mthread"):
        n    = size
        def mat():
            return " ".join(
                str(rng.randint(-10, 10))
                for _ in range(n * n)
            )
        rows_a = "\n".join(
            " ".join(str(rng.randint(-10, 10)) for _ in range(n))
            for _ in range(n)
        )
        rows_b = "\n".join(
            " ".join(str(rng.randint(-10, 10)) for _ in range(n))
            for _ in range(n)
        )
        return f"{n}\n{rows_a}\n{rows_b}\n"

    if algo == "huffman":
        n    = size
        # توزیع غیریکنواخت مثل متن انگلیسی
        weights = [13,9,8,7,6,6,6,5,5,4,4,3,3,3,3,2,2,2,2,1,
                   1,1,1,1,1,1]
        chars   = list(string.ascii_lowercase)
        text    = "".join(rng.choices(chars, weights=weights, k=n))
        return f"{text}\n"

    raise ValueError(f"Unknown algorithm: {algo}")


def apply_cap(algo, lang, sizes):
    """اعمال سقف ورودی برای زبان‌های کند"""
    caps = CAPS.get(lang, {})
    if algo not in caps:
        return sizes
    cap = caps[algo]
    result = []
    for s in sizes:
        if isinstance(s, tuple):
            if isinstance(cap, tuple):
                if s[0] <= cap[0]:
                    result.append(s)
            else:
                result.append(s)
        else:
            if s <= cap:
                result.append(s)
    return result if result else [sizes[0]]


# ══════════════════════════════════════════════
#  COMPILER
# ══════════════════════════════════════════════
def compile_program(lang: str, algo: str, mode: str) -> dict:
    """
    mode: 'debug' یا 'release'
    برمی‌گردونه: {'success': bool, 'bin': Path or None, 'error': str}
    """
    cfg     = LANGUAGES[lang]
    ext     = cfg["ext"]
    src     = ALGO_DIR / lang / f"{algo}.{ext}"

    if not src.exists():
        return {"success": False, "bin": None, "error": f"Source not found: {src}"}

    if not cfg["compiled"]:
        return {"success": True, "bin": src, "error": ""}

    out_dir  = BUILD_DEBUG if mode == "debug" else BUILD_REL
    lang_dir = out_dir / lang
    lang_dir.mkdir(parents=True, exist_ok=True)

    if lang == "java":
        # Java: compile به .class
        tmpl  = cfg[f"compile_{mode}"]
        cmd   = tmpl.format(src=src, outdir=lang_dir)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return {"success": False, "bin": None, "error": result.stderr}
        classname = _java_classname(algo)
        return {"success": True, "bin": lang_dir, "classname": classname, "error": ""}

    if lang == "haskell":
        # Haskell آرتیفکت‌های اضافه تولید می‌کنه
        bin_path = lang_dir / algo
        tmpl     = cfg[f"compile_{mode}"]
        cmd      = tmpl.format(src=src, out=bin_path)
        result   = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                                  cwd=lang_dir)
        if result.returncode != 0:
            return {"success": False, "bin": None, "error": result.stderr}
        return {"success": True, "bin": bin_path, "error": ""}

    bin_path = lang_dir / algo
    tmpl     = cfg[f"compile_{mode}"]
    if cfg.get("no_opt_flag") and mode == "release":
        tmpl = cfg["compile_debug"]  # Java: همون کامپایله
    cmd = tmpl.format(src=src, out=bin_path)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return {"success": False, "bin": None, "error": result.stderr}
    return {"success": True, "bin": bin_path, "error": ""}


def _java_classname(algo: str) -> str:
    """mergesort → Mergesort"""
    parts = algo.split("_")
    return "".join(p.capitalize() for p in parts)


def _build_run_cmd(lang: str, algo: str, mode: str, bin_path) -> list:
    cfg  = LANGUAGES[lang]
    tmpl = cfg.get(f"run_{mode}", cfg["run"]) if mode == "release" else cfg["run"]

    if lang == "java":
        classname = _java_classname(algo)
        cmd_str   = tmpl.format(outdir=bin_path, classname=classname)
    elif cfg["compiled"]:
        cmd_str = str(bin_path)
    else:
        src = ALGO_DIR / lang / f"{algo}.{cfg['ext']}"
        cmd_str = tmpl.format(src=src)

    cmd = cmd_str.split()
    if USE_TASKSET:
        cmd = ["taskset", "-c", TASKSET_CPUS] + cmd
    return cmd


# ══════════════════════════════════════════════
#  RESOURCE MONITOR
# ══════════════════════════════════════════════
class ResourceMonitor:
    """مانیتور RAM و CPU در یک thread جداگانه"""

    def __init__(self, pid: int, interval: float = 0.05):
        self.pid      = pid
        self.interval = interval
        self.peak_ram = 0       # bytes
        self.cpu_samples = []
        self._stop    = threading.Event()
        self._thread  = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop.set()
        self._thread.join()

    def _run(self):
        try:
            proc = psutil.Process(self.pid)
            while not self._stop.is_set():
                try:
                    mem = proc.memory_info().rss
                    cpu = proc.cpu_percent(interval=None)
                    if mem > self.peak_ram:
                        self.peak_ram = mem
                    self.cpu_samples.append(cpu)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break
                time.sleep(self.interval)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    @property
    def avg_cpu(self) -> float:
        return statistics.mean(self.cpu_samples) if self.cpu_samples else 0.0

    @property
    def peak_ram_mb(self) -> float:
        return self.peak_ram / (1024 * 1024)


# ══════════════════════════════════════════════
#  SINGLE RUN
# ══════════════════════════════════════════════
def run_once(cmd: list, stdin_data: str) -> dict:
    """
    یک اجرا — برمی‌گردونه:
    {
      'wall_ms': float,
      'internal_ms': float,   ← از stderr برنامه
      'peak_ram_mb': float,
      'avg_cpu': float,
      'status': 'ok' | 'timeout' | 'error',
      'stdout': str,
    }
    """
    result = {
        "wall_ms": 0.0,
        "internal_ms": 0.0,
        "peak_ram_mb": 0.0,
        "avg_cpu": 0.0,
        "status": "ok",
        "stdout": "",
    }

    try:
        t0  = time.perf_counter()
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        monitor = ResourceMonitor(proc.pid)
        monitor.start()

        try:
            stdout, stderr = proc.communicate(
                input=stdin_data, timeout=TIMEOUT
            )
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
            monitor.stop()
            result["status"] = "timeout"
            result["wall_ms"] = TIMEOUT * 1000
            return result

        wall_ms = (time.perf_counter() - t0) * 1000
        monitor.stop()

        if proc.returncode != 0:
            result["status"] = "error"
            result["wall_ms"] = wall_ms
            return result

        # زمان داخلی از stderr
        internal_ms = 0.0
        if stderr.strip():
            try:
                internal_ms = float(stderr.strip().split("\n")[0])
            except ValueError:
                pass

        result["wall_ms"]      = round(wall_ms, 3)
        result["internal_ms"]  = round(internal_ms, 3)
        result["peak_ram_mb"]  = round(monitor.peak_ram_mb, 2)
        result["avg_cpu"]      = round(monitor.avg_cpu, 1)
        result["stdout"]       = stdout.strip()

    except Exception as e:
        result["status"] = "error"

    return result


# ══════════════════════════════════════════════
#  BENCHMARK ONE COMBO
# ══════════════════════════════════════════════
def benchmark(lang: str, algo: str, size, mode: str, bin_info: dict) -> dict:
    """
    TOTAL_RUNS بار اجرا می‌کنه.
    WARMUP_RUNS اول دور انداخته می‌شن.
    median و stdev از بقیه حساب می‌شه.
    """
    cmd        = _build_run_cmd(lang, algo, mode, bin_info.get("bin"))
    stdin_data = gen_input(algo, size)

    records = []
    for i in range(TOTAL_RUNS):
        res = run_once(cmd, stdin_data)
        if i < WARMUP_RUNS:
            continue          # warmup — دور بینداز
        records.append(res)
        time.sleep(SLEEP_BETWEEN)

    # خلاصه آماری
    def extract(key):
        return [r[key] for r in records
                if r["status"] == "ok"]

    wall_vals     = extract("wall_ms")
    internal_vals = extract("internal_ms")
    ram_vals      = extract("peak_ram_mb")
    cpu_vals      = extract("avg_cpu")

    def safe_median(lst):
        return round(statistics.median(lst), 3) if lst else -1

    def safe_stdev(lst):
        return round(statistics.stdev(lst), 3) if len(lst) >= 2 else 0

    timeout_count = sum(1 for r in records if r["status"] == "timeout")
    error_count   = sum(1 for r in records if r["status"] == "error")

    # status کلی
    if timeout_count > len(records) // 2:
        status = "timeout"
    elif error_count == len(records):
        status = "error"
    else:
        status = "ok"

    size_str = f"{size[0]}v_{size[1]}e" if isinstance(size, tuple) else str(size)

    return {
        "language":        lang,
        "algorithm":       algo,
        "mode":            mode,
        "input_size":      size_str,
        "status":          status,
        "wall_median_ms":  safe_median(wall_vals),
        "wall_stdev_ms":   safe_stdev(wall_vals),
        "internal_median_ms": safe_median(internal_vals),
        "internal_stdev_ms":  safe_stdev(internal_vals),
        "peak_ram_mb":     safe_median(ram_vals),
        "avg_cpu_pct":     safe_median(cpu_vals),
        "timeout_runs":    timeout_count,
        "error_runs":      error_count,
        "measured_runs":   len(records),
    }


# ══════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════
def main():
    ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_csv = RESULTS_DIR / f"benchmark_{ts}.csv"

    ALGOS = list(SIZES.keys())
    MODES = ["debug", "release"]

    fieldnames = [
        "language", "algorithm", "mode", "input_size",
        "status",
        "wall_median_ms", "wall_stdev_ms",
        "internal_median_ms", "internal_stdev_ms",
        "peak_ram_mb", "avg_cpu_pct",
        "timeout_runs", "error_runs", "measured_runs",
    ]

    print(f"\n{'='*60}")
    print(f"  Benchmark Runner — {ts}")
    print(f"  Timeout: {TIMEOUT}s | Runs: {TOTAL_RUNS} ({WARMUP_RUNS} warmup)")
    print(f"  Output: {out_csv}")
    print(f"{'='*60}\n")

    # ── مرحله ۱: کامپایل همه زبان‌های compiled ──
    print("[ COMPILE ]")
    compile_cache = {}   # (lang, algo, mode) → bin_info

    for lang, cfg in LANGUAGES.items():
        for algo in ALGOS:
            src = ALGO_DIR / lang / f"{algo}.{cfg['ext']}"
            if not src.exists():
                continue
            for mode in MODES:
                key = (lang, algo, mode)
                if not cfg["compiled"]:
                    compile_cache[key] = {"bin": src, "success": True}
                    continue
                print(f"  {lang:10} {algo:25} [{mode}] ... ", end="", flush=True)
                info = compile_program(lang, algo, mode)
                compile_cache[key] = info
                print("OK" if info["success"] else f"FAIL: {info['error'][:60]}")

    # ── مرحله ۲: اجرای benchmark ──
    print(f"\n[ BENCHMARK ]")
    total_combos = sum(
        len(apply_cap(algo, lang, SIZES[algo])) * 2   # 2 mode
        for lang in LANGUAGES
        for algo in ALGOS
        if (ALGO_DIR / lang / f"{LANGUAGES[lang]['ext']}").exists() or True
    )

    rows    = []
    done    = 0

    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for algo in ALGOS:
            for lang in LANGUAGES.keys():
                src = ALGO_DIR / lang / f"{LANGUAGES[lang]['ext']}"
                # بررسی وجود فایل
                real_src = ALGO_DIR / lang / \
                    f"{algo}.{LANGUAGES[lang]['ext']}"
                if not real_src.exists():
                    continue

                sizes = apply_cap(algo, lang, SIZES[algo])

                for mode in MODES:
                    key      = (lang, algo, mode)
                    bin_info = compile_cache.get(key, {})

                    if bin_info and not bin_info.get("success", True):
                        print(f"  SKIP (compile failed): {lang}/{algo} [{mode}]")
                        continue

                    for size in sizes:
                        done += 1
                        size_str = (f"{size[0]}v_{size[1]}e"
                                    if isinstance(size, tuple)
                                    else str(size))
                        print(
                            f"  [{done:4d}] {lang:10} {algo:25}"
                            f" {size_str:15} [{mode}] ... ",
                            end="", flush=True
                        )

                        row = benchmark(lang, algo, size, mode, bin_info)
                        rows.append(row)
                        writer.writerow(row)
                        f.flush()

                        status_sym = {
                            "ok":      "✓",
                            "timeout": "T",
                            "error":   "✗",
                        }.get(row["status"], "?")

                        print(
                            f"{status_sym}  "
                            f"wall={row['wall_median_ms']:8.1f}ms  "
                            f"ram={row['peak_ram_mb']:6.1f}MB  "
                            f"cpu={row['avg_cpu_pct']:5.1f}%"
                        )

    # ── مرحله ۳: خلاصه ──
    print(f"\n{'='*60}")
    print(f"  تمام شد. {len(rows)} نتیجه ذخیره شد.")
    ok      = sum(1 for r in rows if r["status"] == "ok")
    timeouts= sum(1 for r in rows if r["status"] == "timeout")
    errors  = sum(1 for r in rows if r["status"] == "error")
    print(f"  ✓ OK: {ok}   T TIMEOUT: {timeouts}   ✗ ERROR: {errors}")
    print(f"  CSV: {out_csv}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()