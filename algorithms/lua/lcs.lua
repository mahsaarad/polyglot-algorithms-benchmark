local function lcs(a, b)
    local n, m = #a, #b
    local prev = {}
    local curr = {}
    for j = 0, m do prev[j] = 0; curr[j] = 0 end

    for i = 1, n do
        local ai = a:sub(i, i)
        for j = 1, m do
            if ai == b:sub(j, j) then
                curr[j] = prev[j-1] + 1
            else
                curr[j] = curr[j-1] > prev[j] and curr[j-1] or prev[j]
            end
        end
        prev, curr = curr, prev
        for j = 0, m do curr[j] = 0 end
    end
    return prev[m]
end

local function main()
    local a   = io.read("*l")
    local b   = io.read("*l")

    local start  = os.clock()
    local result = lcs(a, b)
    local ms     = (os.clock() - start) * 1000

    print(result)
    io.stderr:write(string.format("%.3f\n", ms))
end

main()