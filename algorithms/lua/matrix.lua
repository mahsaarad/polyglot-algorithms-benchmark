local function matmul(A, B, n)
    local C = {}
    for i = 1, n do
        C[i] = {}
        for j = 1, n do C[i][j] = 0 end
    end

    for i = 1, n do
        for k = 1, n do
            local aik = A[i][k]
            for j = 1, n do
                C[i][j] = C[i][j] + aik * B[k][j]
            end
        end
    end
    return C
end

local function main()
    local n   = tonumber(io.read("*l"))
    local A, B = {}, {}

    for i = 1, n do
        A[i] = {}
        local line = io.read("*l")
        local j = 1
        for v in line:gmatch("%S+") do
            A[i][j] = tonumber(v); j = j + 1
        end
    end
    for i = 1, n do
        B[i] = {}
        local line = io.read("*l")
        local j = 1
        for v in line:gmatch("%S+") do
            B[i][j] = tonumber(v); j = j + 1
        end
    end

    local start = os.clock()
    local C     = matmul(A, B, n)
    local ms    = (os.clock() - start) * 1000

    local checksum = 0
    for i = 1, n do
        for j = 1, n do checksum = checksum + C[i][j] end
    end

    print(checksum)
    io.stderr:write(string.format("%.3f\n", ms))
end

main()