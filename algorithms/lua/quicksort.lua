local function partition(arr, l, r)
    local pivot, i = arr[r], l
    for j = l, r - 1 do
        if arr[j] <= pivot then
            arr[i], arr[j] = arr[j], arr[i]
            i = i + 1
        end
    end
    arr[i], arr[r] = arr[r], arr[i]
    return i
end

local function quicksort(arr, l, r)
    if l >= r then return end
    local p = partition(arr, l, r)
    quicksort(arr, l, p - 1)
    quicksort(arr, p + 1, r)
end

local function main()
    local n   = tonumber(io.read("*l"))
    local arr = {}
    local i   = 1
    for v in io.read("*l"):gmatch("%S+") do
        arr[i] = tonumber(v); i = i + 1
    end

    local start = os.clock()
    quicksort(arr, 1, n)
    local ms = (os.clock() - start) * 1000

    print(table.concat(arr, " "))
    io.stderr:write(string.format("%.3f\n", ms))
end

main()