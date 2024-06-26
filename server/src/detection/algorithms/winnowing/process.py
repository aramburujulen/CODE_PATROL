import numpy as np
from .fingerprints import form_fingerprints, find_fingerprint_overlaps
from .kgrams import form_hashed_kgrams
from .tokenize import tokenize
from .winnow import winnow
import math

#
# Pre:---
# Post: Función principal para la comparación de código. Toma dos ficheros como parámetro y sigue los siguientes pasos:
# 1. Transorma a tokens su contenido, recibiendo la lista de tokens y sus posiciones originales.
# 2. Crea los kgrams (subsecuencias de longitud k) y calcula sus huellas 
# 3. Busca cualquier intersección entre los valores de sus huellas, y si hay las devuelve con sus índices.
# 4. Con esos índices, obtiene las poiciones respectivas en los códigos fuente.
# 5. Calcula el porcentaje de tokens compartidos entre tokens totales para averiguar rango de tokens propios en el otro archivo
# 6. Prepara el código a devolver, es decir, con los indices sabemos donde empieza y acaba la copia, así que hacemos highlight de esas partes
# 7. Devuelve el resultado
# params: f1, f2, k default 25
#
def compare_files(f1, f2, k = 25):
    code1 = f1.content
    code2 = f2.content

    print("Comparing: " + f1.name + " and " + f2.name)
    tokens1, positions1 = tokenize(f1)
    tokens2, positions2 = tokenize(f2)


    hashes1, idx1 = form_fingerprints(*winnow(form_hashed_kgrams(tokens1, k), 1))

    hashes2, idx2 = form_fingerprints(*winnow(form_hashed_kgrams(tokens2, k), 1))

    copied_idx1, copied_idx2 = find_fingerprint_overlaps(hashes1, hashes2, idx1, idx2)
    
    pos1 = get_copied_code_pos(copied_idx1, k)
    pos2 = get_copied_code_pos(copied_idx2, k)

    token_overlap1 = np.sum(pos1[1] - pos1[0])
    token_overlap2 = np.sum(pos2[1] - pos2[0])

    sim1 = round(token_overlap1 / get_winnowed_tokens(idx1, k, len(tokens1)) * 100, 2)
    sim2 = round(token_overlap2 / get_winnowed_tokens(idx2, k, len(tokens2)) * 100, 2)

    #print("Percentage of similarity in : " + f1.name + " " + str(sim1) + "%")
    #print("Percentage of similarity in  : " + f2.name + " " + str(sim2) + "%")

    if len(positions1) > 0:
        indices1 = np.clip(np.searchsorted(positions1[:, 0], pos1), 0, len(positions1) - 1)
        pos1 += positions1[indices1, 1]

    if len(positions2) > 0:
        indices2 = np.clip(np.searchsorted(positions2[:, 0], pos2), 0, len(positions2) - 1)
        pos2 += positions2[indices2, 1]

    processed_code1 = prepare_code(code1, pos1).replace("\t", "&nbsp;&nbsp;&nbsp;")
    processed_code2 = prepare_code(code2, pos2).replace("\t", "&nbsp;&nbsp;&nbsp;")

    return {"file_1_sub_id": f1.submission_id, "file_2_sub_id": f2.submission_id, "file_1": f1.name, 
            "file_2": f2.name, "sim1": sim1, "sim2": sim2, "processed_code1": processed_code1, "processed_code2": processed_code2}
    

#
# Pre:---
# Post: Función encargada para recolectar las posiciones del código original donde se intuye
# que existe copia desde las ids de los kgrams
# params: idx, k
#
def get_copied_code_pos(idx, k):
    if len(idx) == 0:
        return np.array([[],[]])

    sorted_idx = np.sort(idx)
    next_idx = np.concatenate([sorted_idx[1:], [0]])
    skips = np.where(next_idx - sorted_idx > k - 1)[0]

    slice_starts = np.concatenate([[sorted_idx[0]], sorted_idx[skips + 1]])
    slice_ends = np.concatenate([sorted_idx[skips]+k, [sorted_idx[-1]+k]])

    return np.array([slice_starts, slice_ends])

#
# Pre:---
# Post: Función para obtener la cantidad total de tokens revelados tras el proceso de winnowing.
# esto se usa para que sea dividido entre los tokens de intersección.
# params: idx, k, token_len
#
def get_winnowed_tokens(idx, k, token_len):
    if len(idx) > 0:
        idx_arr = np.concatenate([np.array(i) for i in idx.values()])
    else:
        idx_arr = np.array([], dtype=int)
    coverage = np.zeros(token_len)
    for offset in range(k):
        coverage[idx_arr + offset] = 1
    return np.sum(coverage)

#
# Pre:---
# Post: Método para preparar el código, teniendo el código fuente y los índices de copia, se modifican 
# los intervalos entre los índices para denotarlos como copiados.
# params: content, positions
#
def prepare_code(content, positions):
    curr_pos = 0
    prepared_code = ""
    for pos in range(len(positions[1])):
        start_pos = positions[0, pos]
        end_pos = positions[1, pos]

        normal_code = content[curr_pos : start_pos]
        copied_code = content[start_pos : end_pos]

        print(len(copied_code))

        prepared_code += normal_code + '<span class="bg-danger text-white">' + copied_code + '</span>'
        curr_pos = end_pos

    prepared_code += content[curr_pos :]

    return prepared_code