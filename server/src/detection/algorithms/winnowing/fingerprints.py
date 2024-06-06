import numpy as np

def form_fingerprints(hashes, idx):
    hash_dict = {}
    for hash_val, i in zip(hashes, idx):
        if hash_val not in hash_dict:
            hash_dict[hash_val] = [i]
        else:
            hash_dict[hash_val].append(i)
    return set(hashes), hash_dict


def find_fingerprint_overlaps(hashes1, hashes2, idx1, idx2):
    intersection = hashes1.intersection(hashes2)
    if len(intersection) > 0:
        overlap_1 = np.concatenate([np.array(idx1[i]) for i in intersection])
        overlap_2 = np.concatenate([np.array(idx2[i]) for i in intersection])
        return overlap_1.flatten(), overlap_2.flatten()
    else:
        return np.array([], dtype=int), np.array([], dtype=int)
