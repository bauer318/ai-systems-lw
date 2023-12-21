import numpy as np
from numpy import linalg


# jaccard measure
def calculate_jaccard(v_1: list[bool], v_2: list[bool]):
    # count of true
    a = v_1.count(True)
    b = v_2.count(True)
    c = 0.0
    if a == 0 and b == 0:
        return 0.0
    for i in range(len(v_1)):
        if v_1[i] and v_2[i]:
            c += 1.0
    return 1.0 - c / (a + b - c)


# central moment
def calculate_distance(v_1, v_2, n_pow) -> float:
    result = 0.0
    for i in range(len(v_1)):
        if v_1[i] == 0.0 or v_2[i] == 0.0:
            continue
        result += pow(abs(v_1[i] - v_2[i]), n_pow)
    return pow(result, 1.0 / n_pow)


# euclidean distance
def calculate_euclidean_distance(v_1, v_2) -> float:
    return calculate_distance(v_1, v_2, 2)


# manhattan distance
def calculate_manhattan_distance(v_1, v_2) -> float:
    return calculate_distance(v_1, v_2, 1)


# normalize value
def normalize(field: int, min_field: int, max_field: int) -> float:
    if min_field == max_field:
        return 0.0
    return (field - min_field) / (max_field - min_field)


# reverse measure
def reverse_measure(field_1: int, field_2: int, min_field: int, max_field: int) -> float:
    if field_1 == field_2:
        return 0.0
    return 1.0 / (abs(normalize(field_1, min_field, max_field) - normalize(field_2, min_field, max_field)))


# cosine measure
def calculate_cosine_measure(v_1, v_2) -> float:
    dot_product = np.dot(v_1, v_2)
    norm_v_1 = linalg.norm(v_1)
    norm_v_2 = linalg.norm(v_2)
    if (norm_v_1 * norm_v_2) == 0:
        return 0.0
    return 1.0 - dot_product / (norm_v_1 * norm_v_2)
