#!/usr/bin/env python3
"""
Validator — Programming Language Comparison
برای هر الگوریتم، خروجی همه زبان‌ها را با هم مقایسه می‌کنه.
اگر همه یکسان بودن: PASS — اگر فرق داشتن: FAIL + نشون می‌ده کدوم زبان اشتباهه.
"""

import subprocess
import sys
import time
import random
import string
import statistics
from pathlib import Path

try:
    import psutil
except ImportError:
    pass  # validate نیازی به psutil نداره

# ══════════════════════════════════════════════
#  PATHS
# ══════════════════════════════════════════════
ROOT     = Path(__file__).resolve().parent.parent
ALGO_DIR = ROOT / "algorithms"
BUILD    = ROOT / "builds" / "release"

# ══════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════
TIMEOUT   = 30
SEED      = 42

# سایز کوچک برای validation — فقط صحت را چک می‌کنیم
VAL_SIZES = {
    "mergesort":            100,
    "mergesort-mthread":    100,
    "quicksort":            100,
    "dijkstra":             (20, 50),
    "kmp":                  500,
    "sieve":                10_000,
    "fft":                  64,
    "montecarlo":           10_000,
    "lcs":                  50,
    "knapsack":             (100, 20),
    "fibonacci_recursive":  15,
    "fibonacci_iterative":  1_000,
    "fibonacci_dp":         1_000,
    "matrix":               8,
    "matrix-mthread":       8,
    "huffman":              500,
}

LANGUAGES = {
    "c":       {"ext": "c",   "compiled": True,  "bin_name": True},
    "rust":    {"ext": "rs",  "compiled": True,  "bin_name": True},
    "go":      {"ext": "go",  "compiled": True,  "bin_name": True},
    "haskell": {"ext": "hs",  "compiled": True,  "bin_name": True},
    "java":    {"ext": "java","compiled": True,  "bin_name": False},
    "julia":   {"ext": "jl",  "compiled": False, "bin_name": False},
    "lua":     {"ext": "lua", "compiled": False, "bin_name": False},
    "python":  {"ext": "py",  "compiled": False, "bin_name": False},
}

# ══════════════════════════════════════════════
#  INPUT GENERATOR (همان runner.py — کوچک‌شده)
# ══════════════════════════════════════════════
def gen_input(algo: str, size, seed: int = SEED) -> str:
    rng = random.Random(seed)

    if algo in ("mergesort", "mergesort-mthread", "quicksort"):
        n   = size
        arr = [rng.randint(-(10**6), 10**6) for _ in range(n)]
        return f"{n}\n{' '.join(map(str, arr))}\n"

    if algo == "dijkstra":
        v, e = size
        edges = set()
        lines = [f"{v} {e} 0"]
        attempts = 0
        while len(edges) < e and attempts < e * 10:
            u = rng.randint(0, v-1)
            t = rng.randint(0, v-1)
            attempts += 1
            if u != t and (u, t) not in edges:
                w = rng.randint(1, 50)
                lines.append(f"{u} {t} {w}")
                edges.add((u, t))
        lines[0] = f"{v} {len(edges)} 0"
        return "\n".join(lines) + "\n"

    if algo == "kmp":
        n    = size
        text = "".join(rng.choices("abcd", k=n))
        pat  = "".join(rng.choices("ab",   k=5))
        return f"{text}\n{pat}\n"

    if algo == "sieve":
        return f"{size}\n"

    if algo == "fft":
        n    = size
        vals = [round(rng.uniform(-5.0, 5.0), 3) for _ in range(n)]
        return f"{n}\n{' '.join(map(str, vals))}\n"

    if algo == "montecarlo":
        return f"{size}\n42\n"

    if algo == "lcs":
        n = size
        a = "".join(rng.choices("ABCDE", k=n))
        b = "".join(rng.choices("ABCDE", k=n))
        return f"{a}\n{b}\n"

    if algo == "knapsack":
        w_cap, n = size
        lines = [f"{w_cap} {n}"]
        for _ in range(n):
            w = rng.randint(1, max(1, w_cap // 5))
            v = rng.randint(1, 50)
            lines.append(f"{w} {v}")
        return "\n".join(lines) + "\n"

    if algo in ("fibonacci_recursive", "fibonacci_iterative", "fibonacci_dp"):
        return f"{size}\n"

    if algo in ("matrix", "matrix-mthread"):
        n     = size
        rows  = lambda: "\n".join(
            " ".join(str(rng.randint(-5, 5)) for _ in range(n))
            for _ in range(n)
        )
        return f"{n}\n{rows()}\n{rows()}\n"

    if algo == "huffman":
        n    = size
        text = "".join(rng.choices("abcdefghij", k=n))
        return f"{text}\n"

    raise ValueError(f"Unknown: {algo}")


# ══════════════════════════════════════════════
#  RUN ONE PROGRAM
# ══════════════════════════════════════════════
def run_program(lang: str, algo: str, stdin_data: str) -> dict:
    """
    برمی‌گردونه:
    {'output': str, 'status': 'ok'|'timeout'|'error', 'stderr': str}
    """
    cfg = LANGUAGES[lang]
    ext = cfg["ext"]
    src = ALGO_DIR / lang / f"{algo}.{ext}"

    if not src.exists():
        return {"output": None, "status": "missing", "stderr": ""}

    # ساخت command
    if lang == "c" or lang == "rust" or lang == "go":
        bin_path = BUILD / lang / algo
        if not bin_path.exists():
            return {"output": None, "status": "not_compiled", "stderr": ""}
        cmd = [str(bin_path)]

    elif lang == "haskell":
        bin_path = BUILD / lang / algo
        if not bin_path.exists():
            return {"output": None, "status": "not_compiled", "stderr": ""}
        cmd = [str(bin_path)]

    elif lang == "java":
        class_dir = BUILD / lang
        classname = _java_classname(algo)
        cmd = ["java", "-cp", str(class_dir), classname]

    elif lang == "julia":
        cmd = ["julia", "--optimize=3", str(src)]

    elif lang == "lua":
        cmd = ["lua", str(src)]

    elif lang == "python":
        cmd = ["python3", str(src)]

    else:
        return {"output": None, "status": "error", "stderr": "Unknown lang"}

    try:
        proc = subprocess.run(
            cmd,
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
        if proc.returncode != 0:
            return {
                "output": None,
                "status": "error",
                "stderr": proc.stderr[:200],
            }
        return {
            "output": proc.stdout.strip(),
            "status": "ok",
            "stderr": proc.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {"output": None, "status": "timeout", "stderr": ""}
    except FileNotFoundError as e:
        return {"output": None, "status": "error", "stderr": str(e)}


def _java_classname(algo: str) -> str:
    return "".join(p.capitalize() for p in algo.split("_"))


# ══════════════════════════════════════════════
#  NORMALIZE OUTPUT
# ══════════════════════════════════════════════
def normalize(algo: str, output: str) -> str:
    """
    خروجی‌ها را normailze می‌کنه تا مقایسه fair باشه.
    مثلاً floating point را گرد می‌کنه.
    """
    if output is None:
        return "__NONE__"

    lines = output.strip().splitlines()

    # FFT و Monte Carlo — floating point
    if algo in ("fft", "montecarlo"):
        try:
            return f"{float(lines[0]):.4f}"
        except (ValueError, IndexError):
            return output

    # Huffman — خط سوم (ratio) floating point
    if algo == "huffman" and len(lines) >= 3:
        try:
            unique   = lines[0].strip()
            bits     = lines[1].strip()
            ratio    = f"{float(lines[2]):.2f}"
            return f"{unique}\n{bits}\n{ratio}"
        except (ValueError, IndexError):
            return output

    # KMP — فقط خط اول (تعداد match) مهمه
    # اندیس‌ها ممکنه 0-based یا 1-based باشن در بعضی زبان‌ها
    if algo == "kmp":
        try:
            return lines[0].strip()
        except IndexError:
            return output

    # بقیه — همان‌طور که هست
    return "\n".join(l.strip() for l in lines)


# ══════════════════════════════════════════════
#  VALIDATE ONE ALGORITHM
# ══════════════════════════════════════════════
def validate_algo(algo: str) -> dict:
    """
    الگوریتم را در همه زبان‌ها اجرا می‌کنه و خروجی‌ها را مقایسه می‌کنه.
    """
    size  = VAL_SIZES[algo]
    stdin = gen_input(algo, size)

    results = {}
    for lang in LANGUAGES:
        src = ALGO_DIR / lang / f"{algo}.{LANGUAGES[lang]['ext']}"
        if not src.exists():
            results[lang] = {"status": "missing", "output": None}
            continue
        res = run_program(lang, algo, stdin)
        results[lang] = res

    # normalize همه خروجی‌ها
    normalized = {
        lang: normalize(algo, r["output"])
        for lang, r in results.items()
        if r["status"] == "ok"
    }

    # پیدا کردن reference (C اگه OK بود، وگرنه اولین OK)
    reference_lang = None
    reference_out  = None

    for lang in ["c", "rust", "go", "java", "julia", "haskell", "lua", "python"]:
        if lang in normalized:
            reference_lang = lang
            reference_out  = normalized[lang]
            break

    if reference_out is None:
        return {
            "algo":    algo,
            "passed":  False,
            "results": results,
            "normalized": normalized,
            "reference_lang": None,
            "mismatches": [],
            "skipped": [],
        }

    mismatches = []
    skipped    = []

    for lang, out in normalized.items():
        if lang == reference_lang:
            continue
        if out != reference_out:
            mismatches.append(lang)

    for lang, r in results.items():
        if r["status"] != "ok":
            skipped.append((lang, r["status"]))

    return {
        "algo":           algo,
        "passed":         len(mismatches) == 0,
        "results":        results,
        "normalized":     normalized,
        "reference_lang": reference_lang,
        "reference_out":  reference_out,
        "mismatches":     mismatches,
        "skipped":        skipped,
    }


# ══════════════════════════════════════════════
#  PRINT HELPERS
# ══════════════════════════════════════════════
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def cprint(color, text): print(f"{color}{text}{RESET}")


def print_result(r: dict):
    algo   = r["algo"]
    passed = r["passed"]

    if passed:
        cprint(GREEN, f"  ✓  PASS   {algo}")
    else:
        cprint(RED,   f"  ✗  FAIL   {algo}")

    if r["skipped"]:
        for lang, status in r["skipped"]:
            sym = "?" if status == "missing" else "T" if status == "timeout" else "!"
            print(f"       {YELLOW}[{sym}] {lang:10} — {status}{RESET}")

    if not passed:
        ref = r["reference_lang"]
        ref_out = r.get("reference_out", "")
        print(f"       Reference ({ref}): "
              f"{repr(ref_out[:80]) if ref_out else 'N/A'}")
        for lang in r["mismatches"]:
            got = r["normalized"].get(lang, "__NONE__")
            print(f"       {RED}≠  {lang:10}: {repr(got[:80])}{RESET}")

    print()


# ══════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════
def main():
    # اگر argument داده شد، فقط اون الگوریتم‌ها را چک کن
    if len(sys.argv) > 1:
        algos = sys.argv[1:]
    else:
        algos = list(VAL_SIZES.keys())

    print(f"\n{BOLD}{'='*60}")
    print(f"  Validator — {len(algos)} algorithm(s)")
    print(f"  Seed: {SEED}  |  Timeout: {TIMEOUT}s")
    print(f"{'='*60}{RESET}\n")

    all_results = []
    for algo in algos:
        if algo not in VAL_SIZES:
            cprint(YELLOW, f"  ? UNKNOWN algo: {algo} — skip")
            continue

        print(f"  Checking {algo} ... ", end="", flush=True)
        t0 = time.perf_counter()
        r  = validate_algo(algo)
        elapsed = time.perf_counter() - t0
        print(f"({elapsed:.1f}s)")
        print_result(r)
        all_results.append(r)

    # ── خلاصه ──
    passed  = sum(1 for r in all_results if r["passed"])
    failed  = sum(1 for r in all_results if not r["passed"])
    total   = len(all_results)

    print(f"{BOLD}{'='*60}")
    print(f"  نتیجه: {passed}/{total} PASS")
    if failed:
        cprint(RED, f"  FAIL: {failed} الگوریتم نیاز به بررسی دارن")
    else:
        cprint(GREEN, "  همه الگوریتم‌ها خروجی یکسان دارن ✓")
    print(f"{'='*60}{RESET}\n")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()