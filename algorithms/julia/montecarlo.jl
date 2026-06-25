function lcg_next(s::UInt32)
    s = s * UInt32(1664525) + UInt32(1013904223)
    return Float64(s >> 1) / Float64(UInt32(1) << 31), s
end

function montecarlo(n::Int, seed::UInt32)
    s      = seed
    inside = 0
    for _ in 1:n
        x, s = lcg_next(s)
        y, s = lcg_next(s)
        if x*x + y*y <= 1.0
            inside += 1
        end
    end
    return 4.0 * inside / n
end

function main()
    input = split(read(stdin, String))
    n     = parse(Int,    input[1])
    seed  = parse(UInt32, input[2])

    # JIT warmup
    montecarlo(100, UInt32(1))

    start = time_ns()
    pi_   = montecarlo(n, seed)
    ms    = (time_ns() - start) / 1e6

    println(@sprintf("%.8f", pi_))
    println(stderr, ms)
end

using Printf
main()