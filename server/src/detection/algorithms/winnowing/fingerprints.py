import numpy as np

#
# Pre:---
# Post: Método paraformar los fingerprints de los hasheos realizados. Un fingerprint se refiere a una huella que representa 
# un trozo de código fuente con sus ubicaciones en el código. Esta función crea un diccionario que enlaza
# cada indice de posición en el código con el valor hasheado
# params: hashes, idx
# 
def form_fingerprints(hashes, idx):
    hash_dict = {}
    for hash_val, i in zip(hashes, idx):
        if hash_val not in hash_dict:
            hash_dict[hash_val] = [i]
        else:
            hash_dict[hash_val].append(i)
    return set(hashes), hash_dict

#
# Pre:---
# Post: Este método intenta encontrar intersecciones entre dos conjuntos de huellas mirando que sus valores hasheados sean iguales.
# Si existen intersecciones, las devuelve junto a los índices donde ocurren.
# params: hashes, idx
# 
def find_fingerprint_overlaps(hashes1, hashes2, idx1, idx2):
    intersection = hashes1.intersection(hashes2)
    if len(intersection) > 0:
        overlap_1 = np.concatenate([np.array(idx1[i]) for i in intersection])
        overlap_2 = np.concatenate([np.array(idx2[i]) for i in intersection])
        return overlap_1.flatten(), overlap_2.flatten()
    else:
        return np.array([], dtype=int), np.array([], dtype=int)
