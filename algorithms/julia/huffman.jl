using DataStructures

mutable struct HNode
    freq  :: Int
    ch    :: UInt8
    left  :: Union{HNode, Nothing}
    right :: Union{HNode, Nothing}
end

HNode(f, c) = HNode(f, c, nothing, nothing)

Base.isless(a::HNode, b::HNode) = a.freq < b.freq

function build_codes!(node::HNode, depth::Int, codes::Vector{Int})
    if isnothing(node.left) && isnothing(node.right)
        codes[node.ch + 1] = depth > 0 ? depth : 1
        return
    end
    isnothing(node.left)  || build_codes!(node.left,  depth+1, codes)
    isnothing(node.right) || build_codes!(node.right, depth+1, codes)
end

function huffman(text::String)
    freq = zeros(Int, 256)
    for c in text; freq[UInt8(c)+1] += 1; end

    pq = PriorityQueue{HNode, Int}()
    unique = 0
    for (i, f) in enumerate(freq)
        if f > 0
            n = HNode(f, UInt8(i-1))
            enqueue!(pq, n, f)
            unique += 1
        end
    end

    while length(pq) > 1
        l = dequeue!(pq)
        r = dequeue!(pq)
        p = HNode(l.freq + r.freq, 0x00, l, r)
        enqueue!(pq, p, p.freq)
    end

    codes = zeros(Int, 256)
    isempty(pq) || build_codes!(dequeue!(pq), 0, codes)

    total = sum(freq[i] * codes[i] for i in 1:256 if freq[i] > 0)
    return unique, total
end

function main()
    text = strip(read(stdin, String))
    n    = length(text)

    # JIT warmup
    huffman("abcd")

    start        = time_ns()
    unique, total = huffman(text)
    ms           = (time_ns() - start) / 1e6

    ratio = total / (8.0 * n)
    println(unique)
    println(total)
    println(@sprintf("%.2f", ratio))
    println(stderr, ms)
end

using Printf
main()