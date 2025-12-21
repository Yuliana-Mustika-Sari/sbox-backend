import numpy as np
from math import log2

def entropy(img):
    ent = 0
    for ch in range(3):
        hist = np.bincount(img[:,:,ch].flatten(), minlength=256)
        prob = hist / np.sum(hist)
        prob = prob[prob > 0]
        ent += -np.sum(prob * np.log2(prob))
    return ent / 3

def npcr(img1, img2):
    diff = img1 != img2
    return np.sum(diff) / diff.size * 100

def uaci(img1, img2):
    return np.mean(np.abs(img1.astype(int) - img2.astype(int)) / 255) * 100
