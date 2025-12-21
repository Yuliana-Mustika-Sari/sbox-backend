from .encrypt import encrypt_image

def decrypt_image(cipher_array, key):
    return encrypt_image(cipher_array, key)
