import pandas as pd

from datasetitem import DatasetItem
from reader import get_dataset_array


def convert_value(value):
    if value == "":
        return 0.0
    return float(value)


def get_motorcycle_type(item) -> str:
    if item.landing_height != "" and item.seats != "":
        return "Cruiser"
    elif item.max_speed != "" and item.power != "":
        return "Sport Motorcycle"
    elif item.fuel_tank_capacity != "":
        return "Sport Tourer"
    elif item.cylinder_number != "":
        return "Enduro"
    elif item.load_capacity != "":
        return "Quad Bike"
    elif item.torque != "":
        return "Touring Motorcycle"
    else:
        return "Motocross"


def check_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != matrix[j][i]:
                print(i, j)


def create_measure_distance_dictionary(dataset_array, calculate_measure):
    measure_distance_dictionary = dict(
        [(item_1.name, dict([(item_2.name, calculate_measure(item_1, item_2)) for item_2 in dataset_array]),) for item_1
         in dataset_array])
    return measure_distance_dictionary


def print_measure(dataset_array, calculate_measure):
    for item_1 in dataset_array:
        for item_2 in dataset_array:
            v = calculate_measure(item_1, item_2)
            if v == 0.0:
                # print('***', item_1.name, item_2.name)
                continue
            else:
                if item_1.name == item_2.name:
                    print('Not Zero for ', item_1.name, item_1.brand, ' and ', item_2.name, item_2.brand, v, '**')


def check_max(dataset_array, calculate_measure):
    max_v = 0
    for item_1 in dataset_array:
        for item_2 in dataset_array:
            max_v = max(calculate_measure(item_1, item_2), max_v)

    print(max_v)


def create_measure_distance_matrix(measure_distance_dictionary):
    return pd.DataFrame.from_dict(measure_distance_dictionary)


def get_item_by_name(name: str) -> DatasetItem | None:
    if str == "":
        return None
    items = get_dataset_array()
    for item in items:
        if item.name == name:
            return item
    return None
