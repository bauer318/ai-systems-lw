import numpy as np
from InquirerPy import inquirer
from numpy import linalg

from cli import main_loop
from contentBasedRecomendationSystem.closeness_strategy import ClosenessStrategy
from contentBasedRecomendationSystem.recomendattion_system import RecommendationSystem
from datasetitem import DatasetItem
from map_displayer import display_map
from measure_worker import brand_matrix, color_matrix, get_brand_distance, get_motorcycle_distance, \
    calculate_measure_using_euclidean_distance, calculate_measure_using_cosine_distance
from nlp_demo import test
from qaSystem.question_answering_logical import process_request, loop_main
from qaSystem.question_answering_manager import QuestionAnsweringManager
from qaSystem.test_processing import creates_request
from reader import get_dataset_array
from util import convert_value, get_motorcycle_type, check_matrix, create_measure_distance_dictionary, \
    create_measure_distance_matrix, get_item_by_name


def main():
    while True:
        qa = loop_main()
        if qa == 1:
            return 0


if __name__ == '__main__':
    main()
