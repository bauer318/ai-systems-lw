import numpy as np

from map_displayer import display_map
from measure_worker import brand_matrix, color_matrix, get_brand_distance, get_motorcycle_distance, \
    calculate_measure_using_euclidean_distance, calculate_measure_using_cosine_distance
from reader import get_dataset_array
from util import convert_value, get_motorcycle_type, check_matrix, create_measure_distance_dictionary, \
    create_measure_distance_matrix


def main():
    dataset_array = get_dataset_array()
    display_map(dataset_array, 'Euclidean distance', calculate_measure_using_euclidean_distance)
    display_map(dataset_array, 'Cosine distance', calculate_measure_using_cosine_distance)


if __name__ == '__main__':
    main()
