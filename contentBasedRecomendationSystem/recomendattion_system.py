from typing import Optional

from contentBasedRecomendationSystem.closeness_strategy import ClosenessStrategy
from contentBasedRecomendationSystem.recomendation_strategy import RecommendationStrategy
from contentBasedRecomendationSystem.utils import find_self
from datasetitem import DatasetItem
from filter import Filter
from filter_util import filter_items
from measure_worker import calculate_ranger
from ranger import Ranger
from reader import get_dataset_array
from util import create_measure_distance_dictionary


class RecommendationSystem:
    items = get_dataset_array()
    measure_matrix_dictionary = None
    min_values: Ranger = None
    closeness_strategy: ClosenessStrategy = None
    recommendation_strategy: RecommendationStrategy = None

    def set_closeness_strategy(self, closeness_strategy: ClosenessStrategy):
        self.closeness_strategy = closeness_strategy

    def calculate_measure_func(self, calculate_measure_function):
        self.min_values = calculate_ranger(self.items)
        self.measure_matrix_dictionary = create_measure_distance_dictionary(self.items, calculate_measure_function)

    def do_recommendation(self, items: list[DatasetItem], liked_items: list[DatasetItem],
                          disliked_items: list[DatasetItem], limit: Optional[int]) -> list[DatasetItem]:
        liked_motorcycles_names = self.query_liked_motorcycle_name_weighted(items, liked_items, None)
        disliked_motorcycles_name = self.query_liked_motorcycle_name_weighted(items, disliked_items, None)

        motorcycles_name = []
        for liked_name in liked_motorcycles_names:
            disliked_name = find_self(
                disliked_motorcycles_name, lambda name_: name_[0] == liked_name[0]
            )
            decremented_w = liked_name[1]
            if disliked_name is not None:
                decremented_w -= disliked_name[0]
            motorcycles_name.append((liked_name[0], decremented_w))
        motorcycles_name = sorted(motorcycles_name, key=lambda x: x[1])

        result = []
        for name in motorcycles_name:
            item = find_self(items, lambda item_: item_.name == name[0])
            if item is not None:
                result.append(item)
        if limit is not None:
            result = result[:limit]
        return result

    def query_liked_motorcycle_name_weighted(self, items: list[DatasetItem], liked_items: list[DatasetItem],
                                             limit: Optional[int]) -> list[DatasetItem]:

        for liked_item in liked_items:
            current_row = self.measure_matrix_dictionary[liked_item.name]
            if current_row is None:
                raise Exception("eggs", "spam")

        # initializes result dictionary with default similarity = 0.0 for all pairs item
        result = dict([item.name, 0.0] for item in items)
        # weighting this result dictionary
        self.create_result_dictionary(result, liked_items)
        result = sorted(result.items(), key=lambda x: x[1])
        if limit is not None:
            result = result[:limit]
        print(result)
        return result

    def query_liked_motorcycles(self, liked_items: list[DatasetItem], limit: Optional[int]) -> list[DatasetItem]:
        for liked_item in liked_items:
            row = self.measure_matrix_dictionary[liked_item.name]
            if row is None:
                raise Exception("eggs", "spam")

        result = dict([item, 0.0] for item in self.items)
        self.create_result_dictionary(result, liked_items)

        result = sorted(result.items(), key=lambda x: x[1])
        result = [x[0] for x in result]
        if limit is not None:
            result = result[:limit]

        items = [x for x in self.items if x.name in result]
        return items

    def query_all_items(self, limit: Optional[int]) -> list[DatasetItem]:
        items = [_ for _ in self.items]
        if limit is not None:
            items = items[:limit]
        return items

    def query_items_using_filter(self, filter_element: Filter, limit: Optional[int]) -> list[DatasetItem]:
        items = [_ for _ in self.items]
        items = filter_items(items, filter_element)
        if limit is not None:
            items = items[:limit]

        return items

    def create_result_dictionary(self, result: dict, items: list[DatasetItem]):
        for item in items:
            row = self.measure_matrix_dictionary[item.name]
            for name in row.keys():
                if not result[name] is None:
                    result[name] += row[name]


def get_recommendation_after_filtration(
        recommendation_system: RecommendationSystem,
        liked_items: list[DatasetItem],
        disliked_items: list[DatasetItem],
        filter_element: Filter,
) -> list:
    items = recommendation_system.items
    filtered_items = filter_items(items, filter_element, None)
    filtered_items_names = [item.name for item in filtered_items]
    for liked_item in liked_items:
        if not liked_item.name in filtered_items_names:
            filtered_items.append(liked_item)
    items = recommendation_system.do_recommendation(items, filtered_items, disliked_items, None)
    return items


def get_recommendation_before_filtration(recommendation_system: RecommendationSystem,
                                         liked_items: list[DatasetItem],
                                         disliked_items: list[DatasetItem],
                                         filter_element: Filter, ) -> list:
    items = recommendation_system.items
    items = recommendation_system.do_recommendation(items, liked_items, disliked_items, None)
    items = filter_items(items, filter_element, None)
    return items
