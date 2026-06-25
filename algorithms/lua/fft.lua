local math = math

-- complex ops با table
local function cadd(a, b) return {a[1]+b[1], a[2]+b[2]} end
local function csub(a, b) return {a[1]-b[1], a[2]-b[2]} end
local function cmul(a, b)
    return {a[1]*b[1]-a[2]*b[2], a[1]*b[2]+a[2]*b[1]}
end
local function cabs(a) return math.sqrt(a[1]*a[1] + a[2]*a[2]) end

local function fft(a, n)
    -- bit-reversal
    local j = 0
    for i = 1, n-1 do
        local bit = n >> 1
        while j & bit ~= 0 do j = j ~ bit; bit = bit >> 1 end
        j = j ~ bit
        if i < j then a[i+1], a[j+1] = a[j+1], a[i+1] end
    end
    -- butterfly
    local len = 2
    while len <= n do
        local ang  = 2 * math.pi / len
        local wlen = {math.cos(ang), math.sin(ang)}
        local i = 0
        while i < n do
            local w = {1.0, 0.0}
            for jj = 0, len//2-1 do
                local u = a[i+jj+1]
                local v = cmul(a[i+jj+len//2+1], w)
                a[i+jj+1]       = cadd(u, v)
                a[i+jj+len//2+1]= csub(u, v)
                w = cmul(w, wlen)
            end
            i = i + len
        end
        len = len << 1
    end
end

local function main()
    local n   = tonumber(io.read("*l"))
    local a   = {}
    local idx = 1
    for v in io.read("*l"):gmatch("%S+") do
        a[idx] = {tonumber(v), 0.0}
        idx = idx + 1
    end

    local start = os.clock()
    fft(a, n)
    local ms = (os.clock() - start) * 1000

    local k   = math.min(5, n)
    local sum = 0
    for i = 1, k do sum = sum + cabs(a[i]) end

    print(string.format("%.6f", sum))
    io.stderr:write(string.format("%.3f\n", ms))
end

main()