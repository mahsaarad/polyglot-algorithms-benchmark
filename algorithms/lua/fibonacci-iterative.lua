local MOD = 1000000007

local function fib_iterative(n)
    if n == 0 then return 0 end
    local a, b = 0, 1
    for _ = 2, n do
        a, b = b, (a + b) % MOD
    end
    return b
end

local function main()
    local n      = tonumber(io.read("*l"))
    local start  = os.clock()
    local result = fib_iterative(n)
    local ms     = (os.clock() - start) * 1000

    print(result)
    io.stderr:write(string.format("%.3f\n", ms))
end

main()