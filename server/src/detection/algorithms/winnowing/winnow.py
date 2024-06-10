import numpy as np

#
# Pre:---
# Post: Función para llamar al proceso de winnowing si es necesario.
# Winnowing se define como dividir las huellas digitales (hasheos) y recoger
# las más representativas para reducir la cantidad de datos a procesar,
# lo que mejora la eficiencia. Si la window_size es 1, devuelve las huellas como están
# params: hashes, window_size
#
def winnow(hashes, window_size):

    if window_size == 1:
        selected_hashes = hashes
        selected_idx = np.arange(len(hashes))
    else:
        selected_idx = do_winnow(hashes, window_size)
        selected_hashes = hashes[selected_idx]

    return selected_hashes, selected_idx

#
# Pre:---
# Post: Función para realizar el proceso de winnowing, recorre los hasheos y busca el valor
# más pequeño de hash que será el más representativo ya que representa un valor único.
# params: hashes, window_size
#
def do_winnow(hashes, window_size):
    selected_idx = []

    buffer = np.full(window_size, np.inf)
    r = 0
    min_idx = 0
    for hash_idx, hash_val in enumerate(hashes):
        r = (r + 1) % window_size
        buffer[r] = hash_val

        if min_idx == r:
            i = (r - 1) % window_size
            while i != r:
                if buffer[i] < buffer[min_idx]:
                    min_idx = i
                i = (i - 1) % window_size

            selected_idx.append(hash_idx - ((r - min_idx) % window_size))
        else:
            if buffer[r] < buffer[min_idx]:
                min_idx = r
                selected_idx.append(hash_idx)

    return np.array(selected_idx, dtype=np.int64)