function matmul(A::Matrix{Int64}, B::Matrix{Int64}, n::Int)
    C = zeros(Int64, n, n)
    @inbounds for i in 1:n
        for k in 1:n
            aik = A[i, k]
            for j in 1:n
                C[i, j] += aik * B[k, j]
            end
        end
    end
    return C
end

function main()
    input = split(read(stdin, String))
    idx   = 1
    n     = parse(Int, input[idx]); idx += 1

    A = Matrix{Int64}(undef, n, n)
    B = Matrix{Int64}(undef, n, n)

    for i in 1:n, j in 1:n
        A[i,j] = parse(Int64, input[idx]); idx += 1
    end
    for i in 1:n, j in 1:n
        B[i,j] = parse(Int64, input[idx]); idx += 1
    end

    # JIT warmup
    w = ones(Int64, 2, 2)
    matmul(w, w, 2)

    start    = time_ns()
    C        = matmul(A, B, n)
    ms       = (time_ns() - start) / 1e6

    checksum = sum(C)
    println(checksum)
    println(stderr, ms)
end

main()