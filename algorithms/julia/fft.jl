function fft!(a::Vector{ComplexF64})
    n = length(a)
    # bit-reversal
    j = 0
    for i in 1:n-1
        bit = n >> 1
        while j & bit != 0
            j ⊻= bit
            bit >>= 1
        end
        j ⊻= bit
        if i < j
            a[i+1], a[j+1] = a[j+1], a[i+1]
        end
    end
    # butterfly
    len = 2
    while len <= n
        ang  = 2π / len
        wlen = exp(im * ang)
        i = 1
        while i <= n
            w = ComplexF64(1, 0)
            for jj in 0:len÷2-1
                u = a[i + jj]
                v = a[i + jj + len÷2] * w
                a[i + jj]         = u + v
                a[i + jj + len÷2] = u - v
                w *= wlen
            end
            i += len
        end
        len <<= 1
    end
end

function main()
    input = split(read(stdin, String))
    idx   = 1
    n     = parse(Int, input[idx]); idx += 1
    a     = ComplexF64[parse(Float64, input[idx+i-1]) + 0im for i in 1:n]

    # JIT warmup
    w = ComplexF64[1.0+0im, -1.0+0im]
    fft!(w)

    start = time_ns()
    fft!(a)
    ms = (time_ns() - start) / 1e6

    k   = min(5, n)
    s   = sum(abs(a[i]) for i in 1:k)
    println(@sprintf("%.6f", s))
    println(stderr, ms)
end

using Printf
main()