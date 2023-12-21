from typing import Optional, Any

from datasetitem import DatasetItem
from filter import Filter
from measure_worker import get_measure_for_weight


def filter_min(items: list, get_value_lambda, min_value: Optional[int]) -> list:
    return filter(lambda item: True if (min_value is None) or (get_value_lambda(item) >= min_value) else False, items)


def filter_max(items: list, get_value_lambda, max_value: Optional[int]) -> list:
    return filter(lambda item: True if (max_value is None) or (get_value_lambda(item) <= max_value) else False, items)


def filter_equal(items: list, get_value_lambda, exact_value: Optional[int]) -> list:
    return filter(lambda item: True if (exact_value is None) or (get_value_lambda(item) == exact_value) else False,
                  items)


def filter_items(items: list[DatasetItem], filter_el: Filter, limit: Optional[int]) -> list[DatasetItem]:
    items = filter_min(items, lambda item: item.engine_capacity, filter_el.engine_capacity_min)
    items = filter_max(items, lambda item: item.engine_capacity, filter_el.engine_capacity_max)
    items = filter_min(items, lambda item: item.ground_clearance, filter_el.ground_clearance_min)
    items = filter_max(items, lambda item: item.ground_clearance, filter_el.ground_clearance_max)
    items = filter_min(items, lambda item: item.landing_height, filter_el.landing_height_min)
    items = filter_max(items, lambda item: item.landing_height, filter_el.landing_height_max)
    items = filter_min(items, lambda item: item.seats, filter_el.seats_min)
    items = filter_max(items, lambda item: item.seats, filter_el.seats_max)
    items = filter_min(items, lambda item: item.max_speed, filter_el.max_speed_min)
    items = filter_max(items, lambda item: item.max_speed, filter_el.max_speed_max)
    items = filter_min(items, lambda item: item.power, filter_el.power_min)
    items = filter_max(items, lambda item: item.power, filter_el.power_max)
    items = filter_min(items, lambda item: item.fuel_tanck_capacity, filter_el.fuel_tank_capacity_min)
    items = filter_max(items, lambda item: item.fuel_tanck_capacity, filter_el.fuel_tank_capacity_max)
    items = filter_min(items, lambda item: item.height, filter_el.height_min)
    items = filter_max(items, lambda item: item.height, filter_el.height_max)
    items = filter_min(items, lambda item: item.cylinder_number, filter_el.cylinder_number_min)
    items = filter_max(items, lambda item: item.cylinder_number, filter_el.cylinder_number_max)
    items = filter_min(items, lambda item: item.load_capacity, filter_el.load_capacity_min)
    items = filter_max(items, lambda item: item.load_capacity, filter_el.load_capacity_max)
    items = filter_min(items, lambda item: item.torque, filter_el.torque_min)
    items = filter_max(items, lambda item: item.torque, filter_el.torque_max)
    items = filter_min(items, lambda item: item.trunk_volume, filter_el.trunk_volume_min)
    items = filter_max(items, lambda item: item.trunk_volume, filter_el.trunk_volume_max)

    items = filter_equal(items, lambda item: item.name, filter_el.name)
    items = filter_equal(items, lambda item: item.brand, filter_el.brand)
    items = filter_equal(items, lambda item: item.color, filter_el.color)
    items = filter_equal(items, lambda item: item.exist_navigator, filter_el.exist_navigator)
    items = filter_equal(items, lambda item: item.exist_compressor, filter_el.exist_compressor)
    items = filter_equal(items, lambda item: item.exist_headlight, filter_el.exist_headlight)
    items = filter_equal(items, lambda item: item.exist_turn_signal, filter_el.exist_turn_signal)
    items = filter_equal(items, lambda item: item.transmission, filter_el.transmission)
    items = filter_equal(items, lambda item: item.exist_radio_system, filter_el.exist_radio_system)

    if filter_el.approx_weight is None:
        items = filter_min(items, lambda item: item.weight, filter_el.weight_min)
        items = filter_max(items, lambda item: item.weight, filter_el.weight_max)
    else:
        items = filter_equal(items, lambda item: get_measure_for_weight(item.weight), filter_el.approx_weight)

    if filter_el.limit is not None:
        items = items[:limit]
    return list(items)
