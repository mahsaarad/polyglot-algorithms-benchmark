local function build_freq(text)
    local freq = {}
    for i = 1, #text do
        local c = text:sub(i,i)
        freq[c] = (freq[c] or 0) + 1
    end
    return freq
end

local function build_tree(freq)
    local nodes = {}
    for ch, f in pairs(freq) do
        table.insert(nodes, {freq=f, ch=ch, left=nil, right=nil})
    end

    local function pop_min()
        local mi, mv = 1, nodes[1].freq
        for i = 2, #nodes do
            if nodes[i].freq < mv then mi = i; mv = nodes[i].freq end
        end
        local n = nodes[mi]
        table.remove(nodes, mi)
        return n
    end

    while #nodes > 1 do
        local l = pop_min()
        local r = pop_min()
        table.insert(nodes, {freq=l.freq+r.freq, ch=nil, left=l, right=r})
    end
    return nodes[1]
end

local function build_codes(node, depth, codes)
    if not node then return end
    if not node.left and not node.right then
        codes[node.ch] = depth > 0 and depth or 1
        return
    end
    build_codes(node.left,  depth+1, codes)
    build_codes(node.right, depth+1, codes)
end

local function main()
    local text  = io.read("*l")
    local n     = #text
    local freq  = build_freq(text)

    local start = os.clock()

    local root  = build_tree(freq)
    local codes = {}
    build_codes(root, 0, codes)

    local unique     = 0
    local total_bits = 0
    for ch, f in pairs(freq) do
        unique = unique + 1
        total_bits = total_bits + f * (codes[ch] or 1)
    end

    local ms    = (os.clock() - start) * 1000
    local ratio = total_bits / (8.0 * n)

    print(unique)
    print(total_bits)
    print(string.format("%.2f", ratio))
    io.stderr:write(string.format("%.3f\n", ms))
end

main()