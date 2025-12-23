POLY = 0x11B

def gf_mul(a, b):
    res = 0
    while b:
        if b & 1:
            res ^= a
        a <<= 1
        if a & 0x100:
            a ^= POLY
        b >>= 1
    return res & 0xFF

def gf_inv(a):
    if a == 0:
        return 0
    res = 1
    for _ in range(254):
        res = gf_mul(res, a)
    return res
