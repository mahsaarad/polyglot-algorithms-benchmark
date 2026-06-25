import sys
import time
import heapq

def huffman(text):
    freq = {}
    for c in text: freq[c] = freq.get(c, 0) + 1

    heap  = []
    counter = 0
    for ch, f in freq.items():
        heapq.heappush(heap, (f, counter, ch, None, None))
        counter += 1

    while len(heap) > 1:
        f1, _, c1, l1, r1 = heapq.heappop(heap)
        f2, _, c2, l2, r2 = heapq.heappop(heap)
        heapq.heappush(heap, (f1+f2, counter, None, (f1,c1,l1,r1), (f2,c2,l2,r2)))
        counter += 1

    codes = {}
    def build(node, depth):
        f, _, ch, left, right = node
        if left is None and right is None:
            codes[ch] = depth if depth > 0 else 1
            return
        build(left,  depth+1)
        build(right, depth+1)

    if heap:
        build(heap[0], 0)

    total_bits = sum(freq[c] * codes.get(c, 1) for c in freq)
    return len(freq), total_bits

def main():
    text = sys.stdin.read().strip()
    n    = len(text)

    start          = time.perf_counter()
    unique, total  = huffman(text)
    ms             = (time.perf_counter() - start) * 1000

    ratio = total / (8.0 * n)
    sys.stdout.write(f"{unique}\n{total}\n{ratio:.2f}\n")
    sys.stderr.write(f"{ms:.3f}\n")

if __name__ == "__main__":
    main()