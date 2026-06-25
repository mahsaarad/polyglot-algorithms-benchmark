local function knapsack(W, weights, values, n)
    local dp = {}
    for w = 0, W do dp[w] = 0 end

    for i = 1, n do
        local wi, vi = weights[i], values[i]
        for w = W, wi, -1 do
            local candidate = dp[w - wi] + vi
            if candidate > dp[w] then dp[w] = candidate end
        end
    end
    return dp[W]
end

local function main()
    local first = io.read("*l")
    local W, n  = first:match("(%d+)%s+(%d+)")
    W = tonumber(W); n = tonumber(n)

    local weights = {}
    local values  = {}
    for i = 1, n do
        local line   = io.read("*l")
        local wi, vi = line:match("(%d+)%s+(%d+)")
        weights[i]   = tonumber(wi)
        values[i]    = tonumber(vi)
    end

    local start  = os.clock()
    local result = knapsack(W, weights, values, n)
    local ms     = (os.clock() - start) * 1000

    print(result)
    io.stderr:write(string.format("%.3f\n", ms))
end

main()