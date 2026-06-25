const MOD = 1_000_000_007

function fib_iterative(n::Int)
    n == 0 && return 0
    a, b = 0, 1
    for _ in 2:n
        a, b = b, (a + b) % MOD
    end
    return b
end

function main()
    n = parse(Int, strip(read(stdin, String)))

    fib_iterative(10)  # JIT warmup

    start  = time_ns()
    result = fib_iterative(n)
    ms     = (time_ns() - start) / 1e6

    println(result)
    println(stderr, ms)
end

main()