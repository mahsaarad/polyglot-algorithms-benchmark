const MOD = 1_000_000_007

function fib_dp(n::Int)
    memo = zeros(Int, n + 1)
    n >= 1 && (memo[2] = 1)
    for i in 3:n+1
        memo[i] = (memo[i-1] + memo[i-2]) % MOD
    end
    return memo[n+1]
end

function main()
    n = parse(Int, strip(read(stdin, String)))

    fib_dp(10)  # JIT warmup

    start  = time_ns()
    result = fib_dp(n)
    ms     = (time_ns() - start) / 1e6

    println(result)
    println(stderr, ms)
end

main()