function partition!(arr::Vector{Int64}, l::Int, r::Int)
    pivot, i = arr[r], l
    for j in l:r-1
        if arr[j] <= pivot
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
        end
    end
    arr[i], arr[r] = arr[r], arr[i]
    return i
end

function quicksort!(arr::Vector{Int64}, l::Int, r::Int)
    l >= r && return
    p = partition!(arr, l, r)
    quicksort!(arr, l, p - 1)
    quicksort!(arr, p + 1, r)
end

function main()
    input = split(read(stdin, String))
    n     = parse(Int, input[1])
    arr   = parse.(Int64, input[2:n+1])

    # JIT warmup
    w = copy(arr[1:min(10, n)])
    quicksort!(w, 1, length(w))

    start = time_ns()
    quicksort!(arr, 1, n)
    ms = (time_ns() - start) / 1e6

    println(join(arr, " "))
    println(stderr, ms)
end

main()