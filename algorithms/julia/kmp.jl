function build_lps(pat::String)
    m   = length(pat)
    lps = zeros(Int, m)
    len, i = 0, 2
    while i <= m
        if pat[i] == pat[len+1]
            len += 1
            lps[i] = len
            i += 1
        elseif len > 0
            len = lps[len]
        else
            lps[i] = 0
            i += 1
        end
    end
    return lps
end

function kmp(text::String, pat::String)
    n, m = length(text), length(pat)
    m == 0 && return Int[]
    lps     = build_lps(pat)
    matches = Int[]
    i, j    = 1, 1
    while i <= n
        if text[i] == pat[j]
            i += 1; j += 1
        end
        if j > m
            push!(matches, i - j)
            j = lps[j-1] + 1
        elseif i <= n && text[i] != pat[j]
            j > 1 ? (j = lps[j-1] + 1) : (i += 1)
        end
    end
    return matches
end

function main()
    lines = readlines(stdin)
    text  = strip(lines[1])
    pat   = strip(lines[2])

    # JIT warmup
    kmp("abab", "ab")

    start   = time_ns()
    matches = kmp(text, pat)
    ms      = (time_ns() - start) / 1e6

    println(length(matches))
    println(isempty(matches) ? "" : join(matches .- 1, " "))
    println(stderr, ms)
end

main()