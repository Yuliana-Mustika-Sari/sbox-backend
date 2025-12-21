import hashlib
import numpy as np

def key_to_seed(key: str):
    h = hashlib.sha256(key.encode()).hexdigest()
    # Limit seed to 32-bit range required by numpy.random.seed
    return int(h[:16], 16) & 0xFFFFFFFF

def image_to_array(img):
    return np.array(img, dtype=np.uint8)

def array_to_image(arr):
    from PIL import Image
    return Image.fromarray(arr.astype(np.uint8))

def entropy(arr):
    """Compute Shannon entropy (bits) of an image/array.

    Flattens the array and computes entropy over byte values 0..255.
    """
    a = np.asarray(arr, dtype=np.uint8).ravel()
    if a.size == 0:
        return 0.0
    vals, counts = np.unique(a, return_counts=True)
    probs = counts / counts.sum()
    return float(-np.sum(probs * np.log2(probs)))

def npcr(a, b):
    """Compute NPCR (percentage) between two images/arrays."""
    A = np.asarray(a, dtype=np.uint8)
    B = np.asarray(b, dtype=np.uint8)
    if A.shape != B.shape:
        raise ValueError("Images must have the same shape for NPCR")
    total = A.size
    diff = np.count_nonzero(A != B)
    return (diff / total) * 100.0

def uaci(a, b):
    """Compute UACI (percentage) between two images/arrays."""
    A = np.asarray(a, dtype=np.int32)
    B = np.asarray(b, dtype=np.int32)
    if A.shape != B.shape:
        raise ValueError("Images must have the same shape for UACI")
    diff = np.abs(A - B).sum()
    total = A.size * 255
    return (diff / total) * 100.0
