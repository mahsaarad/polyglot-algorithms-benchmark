local MOD = 1000000007

local function fib_dp(n)
    local memo = {}
    memo[0] = 0
    if n >= 1 then memo[1] = 1 end
    for i = 2, n do
        memo[i] = (memo[i-1] + memo[i-2]) % MOD
    end
    return memo[n]
end

local function main()
    local n      = tonumber(io.read("*l"))
    local start  = os.clock()
    local result = fib_dp(n)
    local ms     = (os.clock() - start) * 1000

    print(result)
    io.stderr:write(string.format("%.3f\n", ms))
end

main()