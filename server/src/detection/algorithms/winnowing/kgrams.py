import numpy as np

def form_hashed_kgrams(string, k):
    hashes = []

    for offset in range(len(string) - k + 1):
        hashes.append(hash(string[offset : offset + k]))
    
    return np.array(hashes)