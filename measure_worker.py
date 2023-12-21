from enum import Enum
import networkx as nx

from datasetitem import DatasetItem
from measure_distance_worker import calculate_euclidean_distance, calculate_jaccard, calculate_cosine_measure
from ranger import Ranger
from util import get_motorcycle_type, convert_value


class WeightMeasure(Enum):
    LargeWeight = 1
    NotVeryLargeWeight = 2
    AverageWeight = 3
    SmallWeight = 4
    VerySmallWeight = 5


motorcycle_graph = nx.Graph()

motorcycle_graph.add_edge("ROOT", "Motorcycle", weight=0.0)

motorcycle_graph.add_edge("Motorcycle", "Road", weight=1.0)
motorcycle_graph.add_edge("Motorcycle", "Off-Road", weight=1.0)
motorcycle_graph.add_edge("Motorcycle", "Dual Sport", weight=1.0)

motorcycle_graph.add_edge("Road", "Cruiser", weight=2.0)
motorcycle_graph.add_edge("Road", "Sport Motorcycle", weight=2.0)
motorcycle_graph.add_edge("Road", "Sport Tourer", weight=2.0)

motorcycle_graph.add_edge("Off-Road", "Motocross", weight=2.0)
motorcycle_graph.add_edge("Off-Road", "Enduro", weight=2.0)
motorcycle_graph.add_edge("Off-Road", "Quad Bike", weight=2.0)

motorcycle_graph.add_edge("Dual Sport", "Touring Motorcycle", weight=2.0)

color_dictionary = {"Black": 0, "Red": 1, "Dark-bleu": 2, "Bleu": 3, "White": 4, "Green": 5, "Yellow": 6, "Grey": 7}

color_matrix = [
    [0.0, 0.3, 0.2, 0.3, 1.0, 0.3, 0.7, 0.6],
    [0.3, 0.0, 0.6, 0.7, 0.7, 0.7, 0.4, 0.5],
    [0.2, 0.6, 0.0, 0.2, 0.9, 0.6, 0.9, 0.7],
    [0.3, 0.7, 0.2, 0.0, 0.7, 0.7, 1.0, 0.5],
    [1.0, 0.7, 0.9, 0.7, 0.0, 0.7, 0.4, 0.5],
    [0.3, 0.7, 0.6, 0.7, 0.7, 0.0, 0.4, 0.5],
    [0.7, 0.4, 0.9, 1.0, 0.4, 0.4, 0.0, 0.5],
    [0.6, 0.5, 0.7, 0.5, 0.5, 0.5, 0.5, 0.0]
]

transmission_dictionary = {"Variator": 0, "Automatic": 1, "Empty": 2}

transmission_matrix = [
    [0.0, 1.0, 1.0],
    [1.0, 0.0, 0.0],
    [1.0, 1.0, 0.0]
]

brand_dictionary = {"Moto": 0, "Yamaha": 1, "BMW": 2, "Honda": 3, "Kawasaki": 4, "Suzuki": 5, "Lifan": 6, "Avenger": 7,
                    "Racer Ranger": 8, "Dakar": 9, "Roliz Sport": 10, "Ducati": 11, "Aprilia": 12, "Xmoto": 13,
                    "GasGas": 14, "Nexus": 15, "Stels": 16, "Irbis": 17, "Russkaya Mehanika": 18, "Victory": 19}

brand_matrix = [
    [0.0, 0.9, 0.7, 0.7, 0.5, 0.9, 0.3, 0.3, 0.4, 0.6, 0.3, 1.0, 0.4, 0.1, 0.7, 0.5, 0.9, 0.2, 0.8, 0.9],
    [0.9, 0.0, 0.2, 0.4, 0.2, 0.5, 0.9, 0.9, 0.7, 0.5, 0.9, 0.3, 0.9, 0.8, 0.9, 0.3, 1.0, 1.0, 1.0, 0.7],
    [0.7, 0.2, 0.0, 0.5, 0.1, 0.1, 0.7, 0.8, 0.5, 0.7, 0.7, 0.2, 0.4, 0.9, 0.9, 0.4, 0.7, 0.7, 0.6, 0.9],
    [0.7, 0.4, 0.5, 0.0, 0.3, 0.2, 0.9, 0.7, 0.7, 0.5, 0.8, 0.3, 0.7, 0.6, 0.7, 0.2, 1.0, 0.9, 0.4, 0.8],
    [0.5, 0.2, 0.1, 0.3, 0.0, 0.5, 0.7, 0.7, 0.8, 0.7, 0.4, 0.5, 0.9, 0.5, 0.9, 0.4, 0.9, 0.7, 0.6, 0.9],
    [0.9, 0.5, 0.1, 0.2, 0.5, 0.0, 0.9, 0.3, 0.2, 0.4, 0.5, 0.4, 0.2, 0.4, 0.5, 0.2, 0.3, 0.4, 0.5, 0.2],
    [0.3, 0.9, 0.7, 0.9, 0.7, 0.9, 0.0, 0.2, 0.5, 0.7, 0.4, 0.6, 0.8, 0.4, 0.3, 0.5, 0.7, 0.8, 0.4, 0.9],
    [0.3, 0.9, 0.8, 0.7, 0.7, 0.3, 0.2, 0.0, 0.4, 0.5, 0.3, 0.7, 0.3, 0.2, 0.4, 0.8, 0.9, 0.7, 0.8, 0.3],
    [0.4, 0.7, 0.5, 0.7, 0.8, 0.2, 0.5, 0.4, 0.0, 0.3, 0.2, 0.9, 0.2, 0.3, 0.7, 0.2, 0.7, 0.8, 0.2, 0.5],
    [0.6, 0.5, 0.7, 0.5, 0.7, 0.4, 0.7, 0.5, 0.3, 0.0, 0.1, 0.9, 0.4, 0.1, 0.4, 0.7, 0.7, 0.8, 0.7, 0.1],
    [0.3, 0.9, 0.7, 0.8, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0, 0.9, 0.5, 0.3, 0.2, 0.9, 0.3, 0.7, 0.9, 0.5],
    [1.0, 0.3, 0.2, 0.3, 0.5, 0.4, 0.6, 0.7, 0.9, 0.9, 0.9, 0.0, 0.9, 0.8, 0.6, 0.8, 0.7, 0.6, 0.4, 0.5],
    [0.4, 0.9, 0.4, 0.7, 0.9, 0.2, 0.8, 0.3, 0.2, 0.4, 0.5, 0.9, 0.0, 0.2, 0.1, 0.3, 0.5, 0.3, 0.2, 0.2],
    [0.1, 0.8, 0.9, 0.6, 0.5, 0.4, 0.4, 0.2, 0.3, 0.1, 0.3, 0.8, 0.2, 0.0, 0.2, 0.4, 0.5, 0.6, 0.7, 0.7],
    [0.7, 0.9, 0.9, 0.7, 0.9, 0.5, 0.3, 0.4, 0.7, 0.4, 0.2, 0.6, 0.1, 0.2, 0.0, 0.3, 0.4, 0.4, 0.4, 0.4],
    [0.5, 0.3, 0.4, 0.2, 0.4, 0.2, 0.5, 0.8, 0.2, 0.7, 0.9, 0.8, 0.3, 0.4, 0.3, 0.0, 0.2, 0.5, 0.7, 0.5],
    [0.9, 1.0, 0.7, 1.0, 0.9, 0.3, 0.7, 0.9, 0.7, 0.7, 0.3, 0.7, 0.5, 0.5, 0.4, 0.2, 0.0, 0.4, 0.7, 0.2],
    [0.2, 1.0, 0.7, 0.9, 0.7, 0.4, 0.8, 0.7, 0.8, 0.8, 0.7, 0.6, 0.3, 0.6, 0.4, 0.5, 0.4, 0.0, 0.2, 0.3],
    [0.8, 1.0, 0.6, 0.4, 0.6, 0.5, 0.4, 0.8, 0.2, 0.7, 0.9, 0.4, 0.2, 0.7, 0.4, 0.7, 0.7, 0.2, 0.0, 0.4],
    [0.9, 0.7, 0.9, 0.8, 0.9, 0.2, 0.9, 0.3, 0.5, 0.1, 0.5, 0.5, 0.2, 0.7, 0.4, 0.5, 0.2, 0.3, 0.4, 0.0],
]

w_jaccard = 0.2

w_color = 0.6
w_transmission = 0.8
w_brand = 0.1
w_tree = 0.4
w_weight = 0.01
w_engine_capacity = 0.2
w_ground_clearance = 0.7
w_landing_height = 0.7
w_seats = 0.7
w_max_speed = 0.7
w_power = 0.7
w_fuel_tank_capacity = 0.7
w_height = 0.7
w_cylinder = 0.7
w_load_capacity = 0.7
w_torque = 0.7
w_trunk_volume = 0.7


def calculate_weight_distance(item_1, item_2) -> float:
    attribute_1 = [item_1.weight]
    attribute_2 = [item_2.weight]
    return calculate_euclidean_distance(attribute_1, attribute_2)


def calculate_engine_capacity_distance(item_1, item_2) -> float:
    attribute_1 = [item_1.engine_capacity]
    attribute_2 = [item_2.engine_capacity]
    return calculate_euclidean_distance(attribute_1, attribute_2)


def calculate_ground_clearance_distance(item_1, item_2) -> float:
    attribute_1 = [convert_value(item_1.ground_clearance)]
    attribute_2 = [convert_value(item_2.ground_clearance)]
    return calculate_euclidean_distance(attribute_1, attribute_2)


def calculate_landing_height_distance(item_1, item_2) -> float:
    attribute_1 = [convert_value(item_1.landing_height)]
    attribute_2 = [convert_value(item_2.landing_height)]
    return calculate_euclidean_distance(attribute_1, attribute_2)


def calculate_seats_distance(item_1, item_2) -> float:
    attribute_1 = [convert_value(item_1.seats)]
    attribute_2 = [convert_value(item_2.seats)]
    return calculate_euclidean_distance(attribute_1, attribute_2)


def calculate_max_speed_distance(item_1, item_2) -> float:
    attribute_1 = [convert_value(item_1.max_speed)]
    attribute_2 = [convert_value(item_2.max_speed)]
    return calculate_euclidean_distance(attribute_1, attribute_2)


def calculate_power_distance(item_1, item_2) -> float:
    attribute_1 = [convert_value(item_1.power)]
    attribute_2 = [convert_value(item_2.power)]
    return calculate_euclidean_distance(attribute_1, attribute_2)


def calculate_fuel_tank_capacity_distance(item_1, item_2) -> float:
    attribute_1 = [convert_value(item_1.fuel_tank_capacity)]
    attribute_2 = [convert_value(item_2.fuel_tank_capacity)]
    return calculate_euclidean_distance(attribute_1, attribute_2)


def calculate_height_distance(item_1, item_2) -> float:
    attribute_1 = [convert_value(item_1.height)]
    attribute_2 = [convert_value(item_2.height)]
    return calculate_euclidean_distance(attribute_1, attribute_2)


def calculate_cylinder_number_distance(item_1, item_2) -> float:
    attribute_1 = [convert_value(item_1.cylinder_number)]
    attribute_2 = [convert_value(item_2.cylinder_number)]
    return calculate_euclidean_distance(attribute_1, attribute_2)


def calculate_load_capacity_distance(item_1, item_2) -> float:
    attribute_1 = [convert_value(item_1.load_capacity)]
    attribute_2 = [convert_value(item_2.load_capacity)]
    return calculate_euclidean_distance(attribute_1, attribute_2)


def calculate_torque_distance(item_1, item_2) -> float:
    attribute_1 = [convert_value(item_1.torque)]
    attribute_2 = [convert_value(item_2.torque)]
    return calculate_euclidean_distance(attribute_1, attribute_2)


def calculate_trunk_volume_distance(item_1, item_2) -> float:
    attribute_1 = [convert_value(item_1.trunk_volume)]
    attribute_2 = [convert_value(item_2.trunk_volume)]

    return calculate_euclidean_distance(attribute_1, attribute_2)


def calculate_cosine_distance(item_1, item_2) -> float:
    attribute_1 = [convert_value(item_1.trunk_volume), convert_value(item_1.weight),
                   convert_value(item_1.engine_capacity), convert_value(item_1.landing_height),
                   convert_value(item_1.seats), convert_value(item_1.max_speed),
                   convert_value(item_1.power), convert_value(item_1.fuel_tank_capacity),
                   convert_value(item_1.height), convert_value(item_1.cylinder_number),
                   convert_value(item_1.load_capacity), convert_value(item_1.torque)]
    attribute_2 = [convert_value(item_2.trunk_volume), convert_value(item_2.weight),
                   convert_value(item_2.engine_capacity), convert_value(item_2.landing_height),
                   convert_value(item_2.seats), convert_value(item_2.max_speed),
                   convert_value(item_2.power), convert_value(item_2.fuel_tank_capacity),
                   convert_value(item_2.height), convert_value(item_2.cylinder_number),
                   convert_value(item_2.load_capacity), convert_value(item_2.torque)]
    return calculate_cosine_measure(attribute_1, attribute_2)


def get_motorcycle_distance(item_1, item_2) -> float:
    return nx.shortest_path_length(motorcycle_graph, source=get_motorcycle_type(item_1),
                                   target=get_motorcycle_type(item_2))


def get_color_distance(item_1, item_2) -> float:
    if item_1.color == "" or item_2.color == "":
        return 1.0
    if (not item_1.color in color_dictionary) or (not item_2.color in color_dictionary):
        return 1.0
    return color_matrix[color_dictionary[item_1.color]][color_dictionary[item_2.color]]


def get_transmission_distance(item_1, item_2) -> float:
    if item_1.transmission == "" or item_2.transmission == "":
        return 1.0
    if (not item_1.transmission in transmission_dictionary) or (not item_2.transmission in transmission_dictionary):
        return 1.0
    return transmission_matrix[transmission_dictionary[item_1.transmission]][
        transmission_dictionary[item_2.transmission]]


def get_brand_distance(item_1, item_2) -> float:
    if item_1.brand == "" or item_2.brand == "":
        return 1.0
    if (not item_1.brand in brand_dictionary) or (not item_2.brand in brand_dictionary):
        return 1.0
    return brand_matrix[brand_dictionary[item_1.brand]][brand_dictionary[item_2.brand]]


def calculate_jaccard_measure(item_1, item_2) -> float:
    attribute_1 = [item_1.exist_navigator, item_1.exist_compressor, item_1.exist_headlight, item_1.exist_turn_signal,
                   item_1.exist_radio_system]
    attribute_2 = [item_2.exist_navigator, item_2.exist_compressor, item_2.exist_headlight, item_2.exist_turn_signal,
                   item_2.exist_radio_system]
    return calculate_jaccard(attribute_1, attribute_2)


def calculate_ranger(items: list[DatasetItem]) -> Ranger:
    ranger = Ranger()
    if len(items) == 0:
        return ranger
    ranger.weight_min = items[0].weight
    ranger.weight_max = items[0].weight
    ranger.engine_capacity_min = items[0].engine_capacity
    ranger.engine_capacity_max = items[0].engine_capacity
    ranger.ground_clearance_min = convert_value(items[0].ground_clearance)
    ranger.ground_clearance_max = convert_value(items[0].ground_clearance)
    ranger.landing_height_min = convert_value(items[0].landing_height)
    ranger.landing_height_max = convert_value(items[0].landing_height)
    ranger.seats_min = convert_value(items[0].seats)
    ranger.seats_max = convert_value(items[0].seats)
    ranger.max_speed_min = convert_value(items[0].max_speed)
    ranger.max_speed_max = convert_value(items[0].max_speed)
    ranger.power_min = convert_value(items[0].power)
    ranger.power_max = convert_value(items[0].power)
    ranger.fuel_tank_capacity_min = convert_value(items[0].fuel_tank_capacity)
    ranger.fuel_tank_capacity_max = convert_value(items[0].fuel_tank_capacity)
    ranger.height_min = convert_value(items[0].height)
    ranger.height_max = convert_value(items[0].height)
    ranger.cylinder_number_min = convert_value(items[0].cylinder_number)
    ranger.cylinder_number_max = convert_value(items[0].cylinder_number)
    ranger.load_capacity_min = convert_value(items[0].load_capacity)
    ranger.load_capacity_max = convert_value(items[0].load_capacity)
    ranger.torque_min = convert_value(items[0].torque)
    ranger.torque_max = convert_value(items[0].torque)
    ranger.trunk_volume_min = convert_value(items[0].trunk_volume)
    ranger.trunk_volume_max = convert_value(items[0].trunk_volume)

    for item in items:
        ranger.weight_min = min(item.weight, ranger.weight_min)
        ranger.weight_max = max(item.weight, ranger.weight_max)
        ranger.engine_capacity_min = min(item.engine_capacity, ranger.engine_capacity_min)
        ranger.engine_capacity_max = max(item.engine_capacity, ranger.engine_capacity_max)
        ranger.ground_clearance_min = min(convert_value(item.engine_capacity), ranger.engine_capacity_min)
        ranger.ground_clearance_max = max(convert_value(item.engine_capacity), ranger.engine_capacity_max)
        ranger.landing_height_min = min(convert_value(item.landing_height), ranger.landing_height_min)
        ranger.landing_height_max = max(convert_value(item.landing_height), ranger.landing_height_max)
        ranger.seats_min = min(convert_value(item.seats), ranger.seats_min)
        ranger.seats_max = max(convert_value(item.seats), ranger.seats_max)
        ranger.max_speed_min = min(convert_value(item.max_speed), ranger.max_speed_min)
        ranger.max_speed_max = max(convert_value(item.max_speed), ranger.max_speed_max)
        ranger.power_min = min(convert_value(item.power), ranger.power_min)
        ranger.power_max = max(convert_value(item.power), ranger.power_max)
        ranger.fuel_tank_capacity_min = min(convert_value(item.fuel_tank_capacity), ranger.fuel_tank_capacity_min)
        ranger.fuel_tank_capacity_max = max(convert_value(item.fuel_tank_capacity), ranger.fuel_tank_capacity_max)
        ranger.height_min = min(convert_value(item.height), ranger.height_min)
        ranger.height_max = max(convert_value(item.height), ranger.height_max)
        ranger.cylinder_number_min = min(convert_value(item.cylinder_number), ranger.cylinder_number_min)
        ranger.cylinder_number_max = max(convert_value(item.cylinder_number), ranger.cylinder_number_max)
        ranger.load_capacity_min = min(convert_value(item.load_capacity), ranger.load_capacity_min)
        ranger.load_capacity_max = max(convert_value(item.load_capacity), ranger.load_capacity_max)
        ranger.torque_min = min(convert_value(item.torque), ranger.torque_min)
        ranger.torque_max = max(convert_value(item.torque), ranger.torque_max)
        ranger.trunk_volume_min = min(convert_value(item.trunk_volume), ranger.trunk_volume_min)
        ranger.trunk_volume_max = max(convert_value(item.trunk_volume), ranger.trunk_volume_max)

    return ranger


def calculate_measure_using_euclidean_distance(item_1, item_2):
    color_distance = get_color_distance(item_1, item_2)
    transmission_distance = get_transmission_distance(item_1, item_2)
    brand_distance = get_brand_distance(item_1, item_2)
    motorcycle_tree_distance = get_motorcycle_distance(item_1, item_2) / 4
    weight_distance = calculate_weight_distance(item_1, item_2) / 340
    engine_capacity_distance = calculate_engine_capacity_distance(item_1, item_2) / 1748.0

    ground_clearance_distance = calculate_ground_clearance_distance(item_1, item_2) / 126.0
    landing_height_distance = calculate_landing_height_distance(item_1, item_2) / 5.0
    seats_distance = calculate_seats_distance(item_1, item_2)
    max_speed_distance = calculate_max_speed_distance(item_1, item_2) / 260.0
    power_distance = calculate_power_distance(item_1, item_2) / 197.0
    fuel_tank_capacity_distance = calculate_fuel_tank_capacity_distance(item_1, item_2) / 9.5
    height_distance = calculate_height_distance(item_1, item_2) / 490.0
    cylinder_number_distance = calculate_cylinder_number_distance(item_1, item_2)
    load_capacity_distance = calculate_load_capacity_distance(item_1, item_2) / 242.69
    torque_distance = calculate_torque_distance(item_1, item_2) / 94.6
    trunk_volume_distance = calculate_trunk_volume_distance(item_1, item_2) / 140.5

    jaccard_distance = calculate_jaccard_measure(item_1, item_2)
    return (
            w_color * color_distance
            + w_transmission * transmission_distance
            + w_brand * brand_distance
            + w_tree * motorcycle_tree_distance
            + w_weight * weight_distance
            + w_engine_capacity * engine_capacity_distance
            + w_ground_clearance * ground_clearance_distance
            + w_landing_height * landing_height_distance
            + w_seats * seats_distance
            + w_max_speed * max_speed_distance
            + w_power * power_distance
            + w_fuel_tank_capacity * fuel_tank_capacity_distance
            + w_height * height_distance
            + w_cylinder * cylinder_number_distance
            + w_load_capacity * load_capacity_distance
            + w_torque * torque_distance
            + w_trunk_volume * trunk_volume_distance
            + w_jaccard * jaccard_distance
    )


def calculate_measure_using_cosine_distance(item_1, item_2):
    color_distance = get_color_distance(item_1, item_2)
    transmission_distance = get_transmission_distance(item_1, item_2)
    brand_distance = get_brand_distance(item_1, item_2)
    motorcycle_tree_distance = get_motorcycle_distance(item_1, item_2) / 4
    cosine_distance = calculate_cosine_distance(item_1, item_2)

    w_cosine = 0.8

    jaccard_distance = calculate_jaccard_measure(item_1, item_2)
    return (
            w_color * color_distance
            + w_transmission * transmission_distance
            + w_brand * brand_distance
            + w_tree * motorcycle_tree_distance
            + w_cosine * cosine_distance
            + w_jaccard * jaccard_distance)
