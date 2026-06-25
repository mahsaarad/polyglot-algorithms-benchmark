function sieve(n::Int)
    is_composite = falses(n + 1)
    is_composite[1] = true
    i = 2
    while i * i <= n
        if !is_composite[i]
            j = i * i
            while j <= n
                is_composite[j] = true
                j += i
            end
        end
        i += 1
    end

    count, last = 0, -1
    for k in 2:n
        if !is_composite[k]
            count += 1
            last   = k
        end
    end
    return count, last
end

function main()
    n = parse(Int, strip(read(stdin, String)))

    # JIT warmup
    sieve(1000)

    start = time_ns()
    count, last = sieve(n)
    ms = (time_ns() - start) / 1e6

    println(count)
    println(last)
    println(stderr, ms)
end

main()