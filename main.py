import numpy as np
from measure_worker import brand_matrix, color_matrix, get_brand_distance, get_motorcycle_distance, \
    calculate_measure_using_euclidean_distance, calculate_measure_using_cosine_distance
from reader import get_dataset_array
from util import convert_value, get_motorcycle_type, check_matrix, create_measure_distance_dictionary, \
    create_measure_distance_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def main():
    measure_distance_dictionary = create_measure_distance_dictionary(get_dataset_array(),
                                                                     calculate_measure_using_euclidean_distance)
    data = create_measure_distance_matrix(measure_distance_dictionary)
    sns.heatmap(data)
    plt.show()


if __name__ == '__main__':
    main()
