from flask import Flask, request, jsonify
from flask_cors import CORS
import base64 , io
from PIL import Image


from analyzer.main import analyze_sbox
from analyzer.nl import nonlinearity as analyze_nl
from analyzer.sac import sac as analyze_sac
from analyzer.du import differential_uniformity as analyze_du
from analyzer.bic import bic_nl as analyze_bic_nl, bic_sac as analyze_bic_sac
from analyzer.lap import lap as analyze_lap
from analyzer.dap import dap as analyze_dap
from analyzer.ad import algebraic_degree as analyze_ad
from analyzer.to import transparency_order as analyze_to
from analyzer.ci import correlation_immunity as analyze_ci
from image_crypto.encrypt import encrypt_image
from image_crypto.decrypt import decrypt_image
from image_crypto.utils import image_to_array, array_to_image, entropy, npcr, uaci , image_histogram_rgb


app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Backend OK"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    sbox = data.get("sbox")

    if not sbox or len(sbox) != 256:
        return jsonify({
            "error": "S-box harus 256 elemen",
            "length": len(sbox) if sbox else 0
        }), 400

    return jsonify(analyze_sbox(sbox))

@app.route("/affine", methods=["POST"])
def affine():
    data = request.get_json()
    matrix = data.get("matrix")
    constant = data.get("constant")

    if not matrix or len(matrix) != 8 or any(len(r) != 8 for r in matrix):
        return jsonify({"error": "Matrix harus 8x8 bit"}), 400

    if not constant or len(constant) != 8:
        return jsonify({"error": "Constant harus 8 bit"}), 400

    # Matrix & constant (MSB -> LSB)
    A = [[int(b) for b in row[::-1]] for row in matrix]
    C = [int(b) for b in constant[::-1]]

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
        return 0 if a == 0 else gf_pow(a, 254)

    def byte_to_bits(x):
        return [(x >> (7 - i)) & 1 for i in range(8)]

    def bits_to_byte(bits):
        b = 0
        for i, bit in enumerate(bits):
            b |= (bit & 1) << (7 - i)
        return b

    def affine_transform(byte):
        in_bits = byte_to_bits(byte)
        out_bits = []

        for i in range(8):
            s = 0
            for j in range(8):
                s ^= A[i][j] & in_bits[j]
            out_bits.append(s ^ C[i])

        return bits_to_byte(out_bits)

    # Generate S-Box
    sbox = [affine_transform(gf_inv(x)) for x in range(256)]

    analysis = {
        "NL": analyze_nl(sbox),
        "SAC": analyze_sac(sbox),
        "BIC_NL": analyze_bic_nl(sbox),
        "BIC_SAC": analyze_bic_sac(sbox),
        "LAP": analyze_lap(sbox),
        "DAP": analyze_dap(sbox),
        "DU": analyze_du(sbox),
        "AD": analyze_ad(sbox),
        "TO": analyze_to(sbox),
        "CI": analyze_ci(sbox),
    }

    return jsonify({
        "sbox": sbox,
        "analysis": analysis
    })


def xor_bytes(data: bytes, key: bytes):
    result = bytearray()
    for i in range(len(data)):
        result.append(data[i] ^ key[i % len(key)])
    return bytes(result)

@app.route("/encrypt", methods=["POST"])
def encrypt():
    data = request.get_json()
    plaintext = data["plaintext"].encode("utf-8")
    key = data["key"].encode("utf-8")

    cipher_bytes = xor_bytes(plaintext, key)
    cipher_b64 = base64.b64encode(cipher_bytes).decode("ascii")

    return jsonify({"ciphertext": cipher_b64})

@app.route("/decrypt", methods=["POST"])
def decrypt():
    data = request.get_json()
    cipher_b64 = data["ciphertext"]
    key = data["key"].encode("utf-8")

    cipher_bytes = base64.b64decode(cipher_b64)
    plain_bytes = xor_bytes(cipher_bytes, key)

    return jsonify({"plaintext": plain_bytes.decode("utf-8")})

@app.route("/encrypt-image", methods=["POST"])
def encrypt_image_api():
    file = request.files["image"]
    key = request.form["key"]

    img = Image.open(file).convert("RGB")
    plain = image_to_array(img)

    cipher = encrypt_image(plain, key)

    # metrics
    ent = entropy(cipher)
    n = npcr(plain, cipher)
    u = uaci(plain, cipher)

    plain_hist = image_histogram_rgb(plain)
    cipher_hist = image_histogram_rgb(cipher)

    out_img = array_to_image(cipher)
    buf = io.BytesIO()
    out_img.save(buf, format="PNG")

    cipher_b64 = base64.b64encode(buf.getvalue()).decode()

    return jsonify({
        "cipher_image": cipher_b64,
        "entropy": round(ent, 4),
        "npcr": round(n, 2),
        "uaci": round(u, 2),
        "plain_hist": plain_hist,
        "cipher_hist": cipher_hist
    })


@app.route("/decrypt-image", methods=["POST"])
def decrypt_image_api():
    file = request.files["image"]
    key = request.form["key"]

    img = Image.open(file).convert("RGB")
    cipher = image_to_array(img)

    plain = decrypt_image(cipher, key)

    out_img = array_to_image(plain)
    buf = io.BytesIO()
    out_img.save(buf, format="PNG")

    plain_b64 = base64.b64encode(buf.getvalue()).decode()

    return jsonify({
        "plain_image": plain_b64
    })

if __name__ == "__main__":
    app.run(debug=True)
