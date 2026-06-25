local function merge(arr, tmp, l, m, r)
    for i = l, r do tmp[i] = arr[i] end
    local i, j, k = l, m + 1, l
    while i <= m and j <= r do
        if tmp[i] <= tmp[j] then arr[k] = tmp[i]; i = i + 1
        else                     arr[k] = tmp[j]; j = j + 1 end
        k = k + 1
    end
    while i <= m do arr[k] = tmp[i]; i = i + 1; k = k + 1 end
    while j <= r do arr[k] = tmp[j]; j = j + 1; k = k + 1 end
end

local function mergesort(arr, tmp, l, r)
    if l >= r then return end
    local m = l + math.floor((r - l) / 2)
    mergesort(arr, tmp, l, m)
    mergesort(arr, tmp, m + 1, r)
    merge(arr, tmp, l, m, r)
end

local function main()
    local n   = tonumber(io.read("*l"))
    local arr = {}
    local i   = 1
    for v in io.read("*l"):gmatch("%S+") do
        arr[i] = tonumber(v); i = i + 1
    end
    local tmp = {}
    for j = 1, n do tmp[j] = 0 end

    local start = os.clock()
    mergesort(arr, tmp, 1, n)
    local ms = (os.clock() - start) * 1000

    print(table.concat(arr, " "))
    io.stderr:write(string.format("%.3f\n", ms))
end

main()