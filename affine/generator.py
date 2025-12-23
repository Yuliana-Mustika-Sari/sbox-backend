from utils.gf import gf_inv

def generate_sbox(matrix, constant):
    A = [[int(b) for b in row] for row in matrix]
    C = [int(b) for b in constant]

    def byte_to_bits(x):
        return [(x >> (7-i)) & 1 for i in range(8)]

    def bits_to_byte(bits):
        return sum(bits[i] << (7-i) for i in range(8))

    sbox = []
    for x in range(256):
        inv = gf_inv(x)
        in_bits = byte_to_bits(inv)
        out = []
        for i in range(8):
            s = sum(A[i][j] & in_bits[j] for j in range(8)) % 2
            out.append(s ^ C[i])
        sbox.append(bits_to_byte(out))
    return sbox
