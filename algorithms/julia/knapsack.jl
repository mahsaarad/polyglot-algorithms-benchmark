function knapsack(W::Int, weights::Vector{Int}, values::Vector{Int})
    n  = length(weights)
    dp = zeros(Int, W + 1)

    for i in 1:n
        wi, vi = weights[i], values[i]
        for w in W:-1:wi
            candidate = dp[w - wi + 1] + vi
            if candidate > dp[w + 1]
                dp[w + 1] = candidate
            end
        end
    end
    return dp[W + 1]
end

function main()
    input = split(read(stdin, String))
    idx   = 1
    W     = parse(Int, input[idx]); idx += 1
    n     = parse(Int, input[idx]); idx += 1

    weights = Vector{Int}(undef, n)
    values  = Vector{Int}(undef, n)
    for i in 1:n
        weights[i] = parse(Int, input[idx]); idx += 1
        values[i]  = parse(Int, input[idx]); idx += 1
    end

    # JIT warmup
    knapsack(10, [1,2,3], [4,5,6])

    start  = time_ns()
    result = knapsack(W, weights, values)
    ms     = (time_ns() - start) / 1e6

    println(result)
    println(stderr, ms)
end

main()