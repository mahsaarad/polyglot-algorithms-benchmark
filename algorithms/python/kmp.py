import sys
import time

def build_lps(pat):
    m   = len(pat)
    lps = [0] * m
    length, i = 0, 1
    while i < m:
        if pat[i] == pat[length]:
            length += 1
            lps[i]  = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps

def kmp(text, pat):
    n, m = len(text), len(pat)
    if m == 0: return []
    lps     = build_lps(pat)
    matches = []
    i = j   = 0
    while i < n:
        if text[i] == pat[j]:
            i += 1; j += 1
        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pat[j]:
            if j: j = lps[j - 1]
            else: i += 1
    return matches

def main():
    data = sys.stdin.read().splitlines()
    text = data[0].strip()
    pat  = data[1].strip()

    start   = time.perf_counter()
    matches = kmp(text, pat)
    ms      = (time.perf_counter() - start) * 1000

    sys.stdout.write(f"{len(matches)}\n")
    sys.stdout.write((" ".join(map(str, matches)) if matches else "") + "\n")
    sys.stderr.write(f"{ms:.3f}\n")

if __name__ == "__main__":
    main()