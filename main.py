import numpy as np
from numpy import linalg

from cli import main_loop
from contentBasedRecomendationSystem.closeness_strategy import ClosenessStrategy
from contentBasedRecomendationSystem.recomendattion_system import RecommendationSystem
from datasetitem import DatasetItem
from map_displayer import display_map
from measure_worker import brand_matrix, color_matrix, get_brand_distance, get_motorcycle_distance, \
    calculate_measure_using_euclidean_distance, calculate_measure_using_cosine_distance
from reader import get_dataset_array
from util import convert_value, get_motorcycle_type, check_matrix, create_measure_distance_dictionary, \
    create_measure_distance_matrix, get_item_by_name


def main():
    likes = []
    dislikes = []

    recommendation_system = RecommendationSystem()
    recommendation_system.set_closeness_strategy(ClosenessStrategy.NearDistinctSeeds)
    recommendation_system.calculate_measure_func(calculate_measure_using_cosine_distance)

    while True:
        rc = main_loop(recommendation_system, likes, dislikes)
        if rc == 1:
            return 0


if __name__ == '__main__':
    main()
