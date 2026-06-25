function lcs(a::String, b::String)
    n, m = length(a), length(b)
    prev = zeros(Int, m + 1)
    curr = zeros(Int, m + 1)

    for i in 1:n
        for j in 1:m
            if a[i] == b[j]
                curr[j+1] = prev[j] + 1
            else
                curr[j+1] = max(curr[j], prev[j+1])
            end
        end
        prev, curr = curr, prev
        fill!(curr, 0)
    end
    return prev[m+1]
end

function main()
    lines = readlines(stdin)
    a     = strip(lines[1])
    b     = strip(lines[2])

    # JIT warmup
    lcs("abc", "ac")

    start  = time_ns()
    result = lcs(a, b)
    ms     = (time_ns() - start) / 1e6

    println(result)
    println(stderr, ms)
end

main()