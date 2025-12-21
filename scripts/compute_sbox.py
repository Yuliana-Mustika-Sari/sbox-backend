from analyzer.main import analyze_sbox

POLY = 0x11B

def gf_mul(a, b):
    res = 0
    while b:
        if b & 1:
            res ^= a
        b >>= 1
        a <<= 1
        if a & 0x100:
            a ^= POLY
    return res & 0xFF

def gf_pow(a, e):
    res = 1
    while e:
        if e & 1:
            res = gf_mul(res, a)
        a = gf_mul(a, a)
        e >>= 1
    return res

def gf_inv(a):
    if a == 0:
        return 0
    return gf_pow(a, 254)

def byte_to_bits_msb(x):
    return [(x >> (7 - i)) & 1 for i in range(8)]

def bits_to_byte_msb(bits):
    b = 0
    for i, bit in enumerate(bits):
        b |= (bit & 1) << (7 - i)
    return b


def generate_affine_sbox(matrix_rows, constant_bits):
    """
    matrix_rows: list[str] of length 8 (each 8 bits)
    constant_bits: str (8 bits)
    """

    A = [[int(b) for b in row] for row in matrix_rows]
    C = [int(b) for b in constant_bits]

    def affine_transform(byte):
        in_bits = byte_to_bits_msb(byte)
        out_bits = []
        for i, row in enumerate(A):
            s = 0
            for j in range(8):
                s ^= row[j] & in_bits[j]
            out_bits.append(s ^ C[i])
        return bits_to_byte_msb(out_bits)

    sbox = [0] * 256
    for x in range(256):
        inv = gf_inv(x)
        sbox[x] = affine_transform(inv)

    analysis = analyze_sbox(sbox)

    return sbox, analysis
