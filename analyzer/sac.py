def sac(sbox):
    n = 8
    total = 0
    for x in range(256):
        for i in range(n):
            flipped = x ^ (1 << i)
            total += bin(sbox[x] ^ sbox[flipped]).count("1")
    return total / (256 * n * n)