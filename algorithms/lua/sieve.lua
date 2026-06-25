local function sieve(n)
    local is_composite = {}
    -- فقط تا 10M برای Lua — بیشتر timeout می‌شه
    for i = 0, n do is_composite[i] = false end
    is_composite[0] = true
    is_composite[1] = true

    local i = 2
    while i * i <= n do
        if not is_composite[i] then
            local j = i * i
            while j <= n do
                is_composite[j] = true
                j = j + i
            end
        end
        i = i + 1
    end

    local count, last = 0, -1
    for k = 2, n do
        if not is_composite[k] then
            count = count + 1
            last  = k
        end
    end
    return count, last
end

local function main()
    local n   = tonumber(io.read("*l"))

    local start         = os.clock()
    local count, last   = sieve(n)
    local ms            = (os.clock() - start) * 1000

    print(count)
    print(last)
    io.stderr:write(string.format("%.3f\n", ms))
end

main()