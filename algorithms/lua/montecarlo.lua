-- LCG با integer 32bit
local function lcg_next(s)
    s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
    return (s >> 1) / 0x80000000, s
end

local function montecarlo(n, seed)
    local s      = seed
    local inside = 0
    for _ = 1, n do
        local x, y
        x, s = lcg_next(s)
        y, s = lcg_next(s)
        if x*x + y*y <= 1.0 then inside = inside + 1 end
    end
    return 4.0 * inside / n
end

local function main()
    local line1 = io.read("*l")
    local line2 = io.read("*l")
    local n     = tonumber(line1)
    local seed  = tonumber(line2)

    local start = os.clock()
    local pi    = montecarlo(n, seed)
    local ms    = (os.clock() - start) * 1000

    print(string.format("%.8f", pi))
    io.stderr:write(string.format("%.3f\n", ms))
end

main()