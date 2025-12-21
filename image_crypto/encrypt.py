import numpy as np
from .utils import key_to_seed

def encrypt_image(img_array, key):
    h, w, c = img_array.shape
    seed = key_to_seed(key)

    np.random.seed(seed)
    keystream = np.random.randint(0, 256, size=(h, w, c), dtype=np.uint8)

    cipher = np.bitwise_xor(img_array, keystream)
    return cipher
