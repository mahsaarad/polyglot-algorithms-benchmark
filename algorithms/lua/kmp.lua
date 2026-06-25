local function build_lps(pat, m)
    local lps = {}
    for i = 1, m do lps[i] = 0 end
    local len, i = 0, 2
    while i <= m do
        if pat:sub(i,i) == pat:sub(len+1,len+1) then
            len = len + 1
            lps[i] = len
            i = i + 1
        elseif len > 0 then
            len = lps[len]
        else
            lps[i] = 0
            i = i + 1
        end
    end
    return lps
end

local function kmp(text, pat)
    local n, m = #text, #pat
    if m == 0 then return {} end
    local lps     = build_lps(pat, m)
    local matches = {}
    local i, j   = 1, 1
    while i <= n do
        if text:sub(i,i) == pat:sub(j,j) then
            i = i + 1; j = j + 1
        end
        if j > m then
            table.insert(matches, i - j - 1)  -- 0-based
            j = lps[j-1] + 1
        elseif i <= n and text:sub(i,i) ~= pat:sub(j,j) then
            if j > 1 then j = lps[j-1] + 1 else i = i + 1 end
        end
    end
    return matches
end

local function main()
    local text = io.read("*l")
    local pat  = io.read("*l")

    local start   = os.clock()
    local matches = kmp(text, pat)
    local ms      = (os.clock() - start) * 1000

    print(#matches)
    if #matches == 0 then
        print("")
    else
        print(table.concat(matches, " "))
    end
    io.stderr:write(string.format("%.3f\n", ms))
end

main()