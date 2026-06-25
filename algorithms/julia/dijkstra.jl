using DataStructures

const INF = typemax(Int64) ÷ 2

function dijkstra(graph::Vector{Vector{Tuple{Int,Int}}}, v::Int, src::Int)
    dist = fill(INF, v)
    dist[src+1] = 0
    pq = PriorityQueue{Int,Int}()
    enqueue!(pq, src+1, 0)

    while !isempty(pq)
        u, d = dequeue_pair!(pq)
        d > dist[u] && continue
        for (to, w) in graph[u]
            nd = d + w
            if nd < dist[to]
                dist[to] = nd
                pq[to] = nd
            end
        end
    end
    return dist
end

function main()
    input = split(read(stdin, String))
    idx = 1
    V   = parse(Int, input[idx]); idx += 1
    E   = parse(Int, input[idx]); idx += 1
    src = parse(Int, input[idx]); idx += 1

    graph = [Vector{Tuple{Int,Int}}() for _ in 1:V]
    for _ in 1:E
        u = parse(Int, input[idx])+1; idx += 1
        t = parse(Int, input[idx])+1; idx += 1
        w = parse(Int, input[idx]);   idx += 1
        push!(graph[u], (t, w))
    end

    # JIT warmup
    g2 = [[(2,1)], []]
    dijkstra(g2, 2, 0)

    start = time_ns()
    dist  = dijkstra(graph, V, src)
    ms    = (time_ns() - start) / 1e6

    println(join(map(d -> d == INF ? -1 : d, dist), " "))
    println(stderr, ms)
end

main()