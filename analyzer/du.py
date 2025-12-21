def differential_uniformity(sbox):
    du = 0
    for dx in range(1, 256):
        counter = {}
        for x in range(256):
            dy = sbox[x] ^ sbox[x ^ dx]
            counter[dy] = counter.get(dy, 0) + 1
        du = max(du, max(counter.values()))
    return du
