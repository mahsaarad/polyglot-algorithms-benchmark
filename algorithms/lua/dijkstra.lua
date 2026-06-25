local INF = math.maxinteger or 2^53

local function dijkstra(graph, V, src)
    local dist = {}
    local vis  = {}
    for i = 1, V do dist[i] = INF; vis[i] = false end
    dist[src] = 0

    -- simple O(V²) برای Lua که heap ندارد
    for _ = 1, V do
        local u, best = -1, INF
        for i = 1, V do
            if not vis[i] and dist[i] < best then
                best = dist[i]; u = i
            end
        end
        if u == -1 then break end
        vis[u] = true
        if graph[u] then
            for _, edge in ipairs(graph[u]) do
                local to, w = edge[1], edge[2]
                local nd = dist[u] + w
                if nd < dist[to] then dist[to] = nd end
            end
        end
    end
    return dist
end

local function main()
    local first = io.read("*l")
    local V, E, src
    V, E, src = first:match("(%d+)%s+(%d+)%s+(%d+)")
    V = tonumber(V); E = tonumber(E); src = tonumber(src) + 1

    local graph = {}
    for i = 1, V do graph[i] = {} end
    for _ = 1, E do
        local line = io.read("*l")
        local u, t, w = line:match("(%d+)%s+(%d+)%s+(%d+)")
        u = tonumber(u)+1; t = tonumber(t)+1; w = tonumber(w)
        table.insert(graph[u], {t, w})
    end

    local start = os.clock()
    local dist  = dijkstra(graph, V, src)
    local ms    = (os.clock() - start) * 1000

    local out = {}
    for i = 1, V do
        out[i] = dist[i] == INF and -1 or dist[i]
    end
    print(table.concat(out, " "))
    io.stderr:write(string.format("%.3f\n", ms))
end

main()