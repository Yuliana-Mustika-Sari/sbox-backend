def walsh_transform(f):
    n = len(f)
    W = [1 - 2*x for x in f]
    h = 1
    while h < n:
        for i in range(0, n, h*2):
            for j in range(i, i+h):
                x = W[j]
                y = W[j+h]
                W[j] = x + y
                W[j+h] = x - y
        h *= 2
    return W
