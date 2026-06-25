#!/usr/bin/env python3
"""
Visualizer — Programming Language Comparison
ورودی: CSV از runner.py
خروجی: نمودارها در results/plots/
"""

import sys
import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# ══════════════════════════════════════════════
#  PATHS
# ══════════════════════════════════════════════
ROOT      = Path(__file__).resolve().parent.parent
RESULTS   = ROOT / "results"
PLOTS_DIR = RESULTS / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# ══════════════════════════════════════════════
#  STYLE
# ══════════════════════════════════════════════
LANG_COLORS = {
    "c":       "#2196F3",   # آبی
    "rust":    "#FF5722",   # نارنجی تیره
    "go":      "#00BCD4",   # فیروزه‌ای
    "haskell": "#9C27B0",   # بنفش
    "java":    "#FF9800",   # نارنجی
    "julia":   "#4CAF50",   # سبز
    "lua":     "#607D8B",   # خاکستری آبی
    "python":  "#FFC107",   # زرد
}

LANG_ORDER = ["c", "rust", "go", "java", "julia", "haskell", "lua", "python"]

ALGO_GROUPS = {
    "مرتب‌سازی":       ["mergesort", "quicksort"],
    "ریاضی":           ["sieve", "fft", "montecarlo",
                        "fibonacci_recursive",
                        "fibonacci_iterative",
                        "fibonacci_dp"],
    "گراف":            ["dijkstra"],
    "رشته":            ["kmp", "huffman"],
    "برنامه‌نویسی پویا": ["lcs", "knapsack"],
    "ماتریس":          ["matrix", "matrix-mthread"],
}

plt.rcParams.update({
    "figure.dpi":        150,
    "savefig.dpi":       150,
    "font.family":       "DejaVu Sans",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.alpha":        0.3,
    "grid.linestyle":    "--",
    "legend.framealpha": 0.9,
    "legend.fontsize":   9,
})


# ══════════════════════════════════════════════
#  LOAD DATA
# ══════════════════════════════════════════════
def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    # فقط ردیف‌های OK
    df = df[df["status"] == "ok"].copy()

    # input_size را عددی کن جایی که ممکنه
    def parse_size(s):
        s = str(s)
        if "v_" in s:
            # dijkstra: "500v_2000e"
            return int(s.split("v_")[0])
        try:
            return int(s)
        except ValueError:
            return None

    df["size_num"] = df["input_size"].apply(parse_size)
    df["language"] = pd.Categorical(
        df["language"], categories=LANG_ORDER, ordered=True
    )
    return df


# ══════════════════════════════════════════════
#  PLOT 1: HEATMAP — زبان در برابر الگوریتم
# ══════════════════════════════════════════════
def plot_heatmap(df: pd.DataFrame, mode: str = "release"):
    sub = df[df["mode"] == mode].copy()

    # برای هر (language, algorithm) میانگین wall_median_ms
    pivot = (
        sub.groupby(["language", "algorithm"])["wall_median_ms"]
        .median()
        .unstack("algorithm")
    )

    # log scale برای خوانایی بهتر
    pivot_log = np.log10(pivot.replace(0, np.nan) + 1)

    algos = sorted(pivot.columns.tolist())
    langs = [l for l in LANG_ORDER if l in pivot.index]
    pivot_log = pivot_log.reindex(index=langs, columns=algos)

    fig, ax = plt.subplots(figsize=(max(14, len(algos)*1.1),
                                    max(6,  len(langs)*0.8)))

    cmap = LinearSegmentedColormap.from_list(
        "perf", ["#1a9850", "#ffffbf", "#d73027"]
    )

    im = ax.imshow(pivot_log.values, cmap=cmap, aspect="auto")

    # محور
    ax.set_xticks(range(len(algos)))
    ax.set_xticklabels(algos, rotation=40, ha="right", fontsize=9)
    ax.set_yticks(range(len(langs)))
    ax.set_yticklabels(langs, fontsize=10)

    # مقدار داخل هر خانه
    for i in range(len(langs)):
        for j in range(len(algos)):
            val = pivot.values[i, j] if i < len(langs) and j < len(algos) else None
            if val is not None and not np.isnan(val):
                txt = f"{val:.0f}" if val >= 10 else f"{val:.1f}"
                ax.text(j, i, txt, ha="center", va="center",
                        fontsize=7.5,
                        color="white" if pivot_log.values[i,j] > 2 else "black")
            else:
                ax.text(j, i, "N/A", ha="center", va="center",
                        fontsize=7, color="#aaa")

    cbar = plt.colorbar(im, ax=ax, fraction=0.02, pad=0.02)
    cbar.set_label("log₁₀(ms + 1)", fontsize=9)

    ax.set_title(
        f"Heatmap — زمان اجرا (ms) — mode: {mode}\n"
        f"سبز = سریع‌تر   |   قرمز = کندتر",
        fontsize=12, pad=14
    )

    plt.tight_layout()
    out = PLOTS_DIR / f"heatmap_{mode}.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  ✓  {out.name}")


# ══════════════════════════════════════════════
#  PLOT 2: LINE CHART — اندازه ورودی در برابر زمان
# ══════════════════════════════════════════════
def plot_scalability(df: pd.DataFrame, mode: str = "release"):
    sub    = df[(df["mode"] == mode) & df["size_num"].notna()].copy()
    algos  = sub["algorithm"].unique()

    for algo in algos:
        adf = sub[sub["algorithm"] == algo].copy()
        if adf["size_num"].nunique() < 2:
            continue

        fig, ax = plt.subplots(figsize=(9, 5))

        for lang in LANG_ORDER:
            ldf = adf[adf["language"] == lang].sort_values("size_num")
            if ldf.empty:
                continue
            ax.plot(
                ldf["size_num"],
                ldf["wall_median_ms"],
                marker="o",
                label=lang,
                color=LANG_COLORS.get(lang, "#999"),
                linewidth=2,
                markersize=5,
            )
            # error band — stdev
            if "wall_stdev_ms" in ldf.columns:
                ax.fill_between(
                    ldf["size_num"],
                    ldf["wall_median_ms"] - ldf["wall_stdev_ms"],
                    ldf["wall_median_ms"] + ldf["wall_stdev_ms"],
                    color=LANG_COLORS.get(lang, "#999"),
                    alpha=0.12,
                )

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("اندازه ورودی (log)", fontsize=10)
        ax.set_ylabel("زمان اجرا — ms (log)", fontsize=10)
        ax.set_title(
            f"Scalability — {algo}  |  mode: {mode}",
            fontsize=12
        )
        ax.legend(loc="upper left", ncol=2)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(
            lambda x, _: f"{int(x):,}"
        ))

        plt.tight_layout()
        out = PLOTS_DIR / f"scalability_{algo}_{mode}.png"
        plt.savefig(out, bbox_inches="tight")
        plt.close()

    print(f"  ✓  scalability_{mode}_*.png  ({len(algos)} charts)")


# ══════════════════════════════════════════════
#  PLOT 3: BOX PLOT — variance بین زبان‌ها
# ══════════════════════════════════════════════
def plot_boxplot(df: pd.DataFrame, mode: str = "release"):
    sub = df[df["mode"] == mode].copy()

    for algo in sub["algorithm"].unique():
        adf = sub[sub["algorithm"] == algo]
        if adf["language"].nunique() < 2:
            continue

        # برای box plot به داده‌های خام نیاز داریم
        # wall_median_ms را به عنوان point estimate استفاده می‌کنیم
        # و stdev را برای simulate کردن distribution
        langs_present = [l for l in LANG_ORDER if l in adf["language"].values]

        fig, ax = plt.subplots(figsize=(10, 5))

        data_per_lang = []
        labels        = []
        colors        = []

        for lang in langs_present:
            ldf = adf[adf["language"] == lang]
            if ldf.empty:
                continue
            vals = ldf["wall_median_ms"].dropna().tolist()
            if vals:
                data_per_lang.append(vals)
                labels.append(lang)
                colors.append(LANG_COLORS.get(lang, "#999"))

        if not data_per_lang:
            plt.close()
            continue

        bp = ax.boxplot(
            data_per_lang,
            patch_artist=True,
            medianprops={"color": "black", "linewidth": 2},
            whiskerprops={"linewidth": 1.5},
            capprops={"linewidth": 1.5},
        )

        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.75)

        ax.set_xticks(range(1, len(labels)+1))
        ax.set_xticklabels(labels, fontsize=10)
        ax.set_ylabel("زمان اجرا — ms", fontsize=10)
        ax.set_title(
            f"Box Plot — {algo}  |  mode: {mode}\n"
            f"variance بین سایزهای مختلف ورودی",
            fontsize=11
        )
        ax.set_yscale("log")

        plt.tight_layout()
        out = PLOTS_DIR / f"boxplot_{algo}_{mode}.png"
        plt.savefig(out, bbox_inches="tight")
        plt.close()

    print(f"  ✓  boxplot_{mode}_*.png")


# ══════════════════════════════════════════════
#  PLOT 4: BAR CHART — debug vs release
# ══════════════════════════════════════════════
def plot_optimization_impact(df: pd.DataFrame):
    """تأثیر -O3 vs debug برای هر زبان × الگوریتم"""

    # فقط زبان‌های compiled که optimization flag دارن
    compiled = ["c", "rust", "go", "haskell"]
    sub      = df[df["language"].isin(compiled)].copy()

    pivot = (
        sub.groupby(["language", "algorithm", "mode"])["wall_median_ms"]
        .median()
        .unstack("mode")
        .dropna()
    )

    if "debug" not in pivot.columns or "release" not in pivot.columns:
        print("  ! optimization chart: داده کافی نیست")
        return

    pivot["speedup"] = pivot["debug"] / pivot["release"]
    pivot            = pivot.reset_index()

    algos = sorted(pivot["algorithm"].unique())
    langs = [l for l in compiled if l in pivot["language"].values]

    fig, ax = plt.subplots(figsize=(max(12, len(algos)*1.2), 5))

    x     = np.arange(len(algos))
    width = 0.8 / len(langs)

    for idx, lang in enumerate(langs):
        ldf = pivot[pivot["language"] == lang]
        ldf = ldf.set_index("algorithm").reindex(algos)
        vals = ldf["speedup"].fillna(1.0).values
        bars = ax.bar(
            x + idx * width - (len(langs)-1)*width/2,
            vals,
            width=width * 0.9,
            label=lang,
            color=LANG_COLORS.get(lang, "#999"),
            alpha=0.85,
        )
        for bar, val in zip(bars, vals):
            if val >= 1.5:
                ax.text(
                    bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 0.05,
                    f"{val:.1f}×",
                    ha="center", va="bottom", fontsize=7.5
                )

    ax.axhline(y=1.0, color="black", linewidth=1, linestyle="--", alpha=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(algos, rotation=35, ha="right", fontsize=9)
    ax.set_ylabel("Speedup  (debug ÷ release)", fontsize=10)
    ax.set_title(
        "تأثیر بهینه‌سازی کامپایلر  |  debug vs -O3\n"
        "بالاتر = release خیلی سریع‌تر از debug",
        fontsize=12
    )
    ax.legend(loc="upper right")

    plt.tight_layout()
    out = PLOTS_DIR / "optimization_impact.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  ✓  {out.name}")


# ══════════════════════════════════════════════
#  PLOT 5: RAM HEATMAP
# ══════════════════════════════════════════════
def plot_ram_heatmap(df: pd.DataFrame, mode: str = "release"):
    sub = df[df["mode"] == mode].copy()

    pivot = (
        sub.groupby(["language", "algorithm"])["peak_ram_mb"]
        .median()
        .unstack("algorithm")
    )

    algos = sorted(pivot.columns.tolist())
    langs = [l for l in LANG_ORDER if l in pivot.index]
    pivot = pivot.reindex(index=langs, columns=algos)

    fig, ax = plt.subplots(figsize=(max(14, len(algos)*1.1),
                                    max(6,  len(langs)*0.8)))

    cmap = LinearSegmentedColormap.from_list(
        "ram", ["#e8f5e9", "#fff9c4", "#b71c1c"]
    )

    im = ax.imshow(pivot.values, cmap=cmap, aspect="auto")

    ax.set_xticks(range(len(algos)))
    ax.set_xticklabels(algos, rotation=40, ha="right", fontsize=9)
    ax.set_yticks(range(len(langs)))
    ax.set_yticklabels(langs, fontsize=10)

    for i in range(len(langs)):
        for j in range(len(algos)):
            val = pivot.values[i, j]
            if not np.isnan(val):
                ax.text(j, i, f"{val:.1f}",
                        ha="center", va="center", fontsize=8,
                        color="white" if val > pivot.values[
                            ~np.isnan(pivot.values)].max() * 0.6
                        else "black")

    cbar = plt.colorbar(im, ax=ax, fraction=0.02, pad=0.02)
    cbar.set_label("Peak RAM (MB)", fontsize=9)

    ax.set_title(
        f"RAM Heatmap — peak memory (MB) — mode: {mode}",
        fontsize=12, pad=14
    )
    plt.tight_layout()
    out = PLOTS_DIR / f"ram_heatmap_{mode}.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  ✓  {out.name}")


# ══════════════════════════════════════════════
#  PLOT 6: MULTITHREADING SPEEDUP
# ══════════════════════════════════════════════
def plot_multithread_speedup(df: pd.DataFrame, mode: str = "release"):
    sub = df[df["mode"] == mode].copy()

    mt_algos = {
        "mergesort":         "mergesort-mthread",
        "matrix":            "matrix-mthread",
    }

    langs = ["c", "rust", "go"]

    fig, axes = plt.subplots(1, len(mt_algos), figsize=(12, 5))
    if len(mt_algos) == 1:
        axes = [axes]

    for ax, (base_algo, mt_algo) in zip(axes, mt_algos.items()):
        base_df = sub[sub["algorithm"] == base_algo]
        mt_df   = sub[sub["algorithm"] == mt_algo]

        if base_df.empty or mt_df.empty:
            ax.set_title(f"{base_algo}\n(داده کافی نیست)")
            continue

        x      = np.arange(len(langs))
        width  = 0.35
        base_vals, mt_vals, speedups = [], [], []

        for lang in langs:
            b = base_df[base_df["language"] == lang]["wall_median_ms"].median()
            m = mt_df[mt_df["language"] == lang]["wall_median_ms"].median()
            base_vals.append(b if not np.isnan(b) else 0)
            mt_vals.append(m   if not np.isnan(m) else 0)
            speedups.append(b/m if (not np.isnan(b) and not np.isnan(m)
                                    and m > 0) else 1.0)

        bars1 = ax.bar(x - width/2, base_vals, width,
                       label="single-thread",
                       color=[LANG_COLORS[l] for l in langs],
                       alpha=0.6)
        bars2 = ax.bar(x + width/2, mt_vals, width,
                       label="multi-thread",
                       color=[LANG_COLORS[l] for l in langs],
                       alpha=1.0)

        for bar, sp in zip(bars2, speedups):
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() * 1.02,
                    f"{sp:.1f}×",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")

        ax.set_xticks(x)
        ax.set_xticklabels(langs, fontsize=10)
        ax.set_ylabel("زمان اجرا — ms", fontsize=9)
        ax.set_title(f"{base_algo}\nsingle vs multi-thread", fontsize=10)
        ax.legend(fontsize=8)

    plt.suptitle(
        f"تأثیر Multi-threading  |  mode: {mode}",
        fontsize=13, y=1.02
    )
    plt.tight_layout()
    out = PLOTS_DIR / f"multithread_speedup_{mode}.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  ✓  {out.name}")


# ══════════════════════════════════════════════
#  PLOT 7: OVERALL RANKING
# ══════════════════════════════════════════════
def plot_overall_ranking(df: pd.DataFrame, mode: str = "release"):
    """
    برای هر زبان، geometric mean زمان نرمال‌شده
    (نسبت به سریع‌ترین زبان در هر الگوریتم)
    """
    sub = df[df["mode"] == mode].copy()

    # برای هر (algorithm, size) نرمال کن به کمترین زمان
    sub["rel_time"] = sub.groupby(["algorithm", "input_size"])[
        "wall_median_ms"
    ].transform(lambda x: x / x.min())

    # geometric mean برای هر زبان
    geo_means = (
        sub.groupby("language")["rel_time"]
        .apply(lambda x: np.exp(np.log(x.clip(lower=0.01)).mean()))
        .sort_values()
    )

    langs  = geo_means.index.tolist()
    values = geo_means.values

    fig, ax = plt.subplots(figsize=(9, 5))

    colors = [LANG_COLORS.get(l, "#999") for l in langs]
    bars   = ax.barh(langs, values, color=colors, alpha=0.85, edgecolor="white")

    for bar, val in zip(bars, values):
        ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
                f"{val:.2f}×",
                va="center", fontsize=10)

    ax.axvline(x=1.0, color="black", linewidth=1.5,
               linestyle="--", alpha=0.6, label="baseline (best)")
    ax.set_xlabel("Geometric Mean  نسبت به سریع‌ترین", fontsize=10)
    ax.set_title(
        f"رتبه‌بندی کلی زبان‌ها  |  mode: {mode}\n"
        f"کمتر = بهتر  |  ۱.۰ = بهترین",
        fontsize=12
    )
    ax.legend(fontsize=9)
    ax.set_xlim(0, max(values) * 1.2)

    plt.tight_layout()
    out = PLOTS_DIR / f"overall_ranking_{mode}.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  ✓  {out.name}")


# ══════════════════════════════════════════════
#  PLOT 8: CPU vs TIME SCATTER
# ══════════════════════════════════════════════
def plot_cpu_vs_time(df: pd.DataFrame, mode: str = "release"):
    sub = df[df["mode"] == mode].copy()

    fig, ax = plt.subplots(figsize=(9, 6))

    for lang in LANG_ORDER:
        ldf = sub[sub["language"] == lang]
        if ldf.empty:
            continue
        ax.scatter(
            ldf["wall_median_ms"],
            ldf["avg_cpu_pct"],
            label=lang,
            color=LANG_COLORS.get(lang, "#999"),
            alpha=0.7,
            s=50,
            edgecolors="white",
            linewidths=0.5,
        )

    ax.set_xscale("log")
    ax.set_xlabel("زمان اجرا — ms (log)", fontsize=10)
    ax.set_ylabel("میانگین CPU %", fontsize=10)
    ax.set_title(
        f"CPU Usage در برابر زمان اجرا  |  mode: {mode}\n"
        f"هر نقطه یک (الگوریتم × سایز)",
        fontsize=11
    )
    ax.legend(loc="upper left", ncol=2, fontsize=9)

    plt.tight_layout()
    out = PLOTS_DIR / f"cpu_vs_time_{mode}.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  ✓  {out.name}")


# ══════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════
def main():
    # پیدا کردن آخرین CSV
    if len(sys.argv) > 1:
        csv_path = Path(sys.argv[1])
    else:
        csvs = sorted(RESULTS.glob("benchmark_*.csv"))
        if not csvs:
            print("هیچ CSV پیدا نشد. اول runner.py را اجرا کن.")
            sys.exit(1)
        csv_path = csvs[-1]

    print(f"\n{'='*60}")
    print(f"  Visualizer")
    print(f"  Input: {csv_path.name}")
    print(f"  Output: {PLOTS_DIR}")
    print(f"{'='*60}\n")

    df = load_csv(csv_path)
    print(f"  {len(df)} ردیف OK لود شد.\n")

    print("[ GENERATING CHARTS ]")

    for mode in ["debug", "release"]:
        print(f"\n  — mode: {mode} —")
        plot_heatmap(df, mode)
        plot_scalability(df, mode)
        plot_boxplot(df, mode)
        plot_ram_heatmap(df, mode)
        plot_multithread_speedup(df, mode)
        plot_overall_ranking(df, mode)
        plot_cpu_vs_time(df, mode)

    plot_optimization_impact(df)

    print(f"\n{'='*60}")
    print(f"  همه نمودارها ذخیره شدن در:")
    print(f"  {PLOTS_DIR}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()