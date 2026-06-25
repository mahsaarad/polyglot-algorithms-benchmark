const MOD = 1_000_000_007

function fib(n::Int)
    n <= 1 && return n
    return (fib(n-1) + fib(n-2)) % MOD
end

function main()
    n = parse(Int, strip(read(stdin, String)))

    # JIT warmup
    fib(10)

    start  = time_ns()
    result = fib(n)
    ms     = (time_ns() - start) / 1e6

    println(result)
    println(stderr, ms)
end

main()