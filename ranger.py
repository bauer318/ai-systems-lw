from dataclasses import dataclass


@dataclass
class Ranger:
    weight_min: int = 0
    weight_max: int = 0
    engine_capacity_min: int = 0
    engine_capacity_max: int = 0
    ground_clearance_min: int = 0
    ground_clearance_max: int = 0
    landing_height_min: int = 0
    landing_height_max: int = 0
    seats_min: int = 0
    seats_max: int = 0
    max_speed_min: int = 0
    max_speed_max: int = 0
    power_min: int = 0
    power_max: int = 0
    fuel_tank_capacity_min: int = 0
    fuel_tank_capacity_max: int = 0
    height_min: int = 0
    height_max: int = 0
    cylinder_number_min: int = 0
    cylinder_number_max: int = 0
    load_capacity_min: int = 0
    load_capacity_max: int = 0
    torque_min: int = 0
    torque_max: int = 0
    trunk_volume_min: int = 0
    trunk_volume_max: int = 0
