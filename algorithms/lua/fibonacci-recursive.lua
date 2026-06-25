local MOD = 1000000007

local function fib(n)
    if n <= 1 then return n end
    return (fib(n-1) + fib(n-2)) % MOD
end

local function main()
    local n     = tonumber(io.read("*l"))
    local start = os.clock()
    local result = fib(n)
    local ms    = (os.clock() - start) * 1000

    print(result)
    io.stderr:write(string.format("%.3f\n", ms))
end

main()