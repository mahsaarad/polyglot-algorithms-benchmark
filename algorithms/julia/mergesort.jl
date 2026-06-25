function merge!(arr::Vector{Int64}, tmp::Vector{Int64}, l::Int, m::Int, r::Int)
    @inbounds tmp[l:r] .= arr[l:r]
    i, j, k = l, m + 1, l
    @inbounds while i <= m && j <= r
        if tmp[i] <= tmp[j]
            arr[k] = tmp[i]; i += 1
        else
            arr[k] = tmp[j]; j += 1
        end
        k += 1
    end
    @inbounds while i <= m; arr[k] = tmp[i]; i += 1; k += 1; end
    @inbounds while j <= r; arr[k] = tmp[j]; j += 1; k += 1; end
end

function mergesort!(arr::Vector{Int64}, tmp::Vector{Int64}, l::Int, r::Int)
    l >= r && return
    m = l + (r - l) ÷ 2
    mergesort!(arr, tmp, l, m)
    mergesort!(arr, tmp, m + 1, r)
    merge!(arr, tmp, l, m, r)
end

function main()
    input = split(read(stdin, String))
    n     = parse(Int, input[1])
    arr   = parse.(Int64, input[2:n+1])
    tmp   = similar(arr)

    # JIT warmup
    w = copy(arr[1:min(10, n)])
    wt = similar(w)
    mergesort!(w, wt, 1, length(w))

    start = time_ns()
    mergesort!(arr, tmp, 1, n)
    ms = (time_ns() - start) / 1e6

    println(join(arr, " "))
    println(stderr, ms)
end

main()