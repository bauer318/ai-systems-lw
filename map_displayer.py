from datasetitem import DatasetItem
from util import create_measure_distance_dictionary, create_measure_distance_matrix
import seaborn as sns
import matplotlib.pyplot as plt


def display_map(dataset_array: [DatasetItem], title, calculate_measure_func):
    measure_distance_dictionary = create_measure_distance_dictionary(dataset_array, calculate_measure_func)
    data = create_measure_distance_matrix(measure_distance_dictionary)
    sns.heatmap(data)
    plt.title(title)
    plt.show()
