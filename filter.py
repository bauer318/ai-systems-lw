from dataclasses import dataclass
from typing import Optional

from weight_measure import WeightMeasure


@dataclass
class Filter:
    name: Optional[str] = None
    brand: Optional[str] = None
    weight_min: Optional[float] = None
    weight_max: Optional[float] = None
    engine_capacity_min: Optional[float] = None
    engine_capacity_max: Optional[float] = None
    color: Optional[str] = None
    ground_clearance_min: Optional[int] = None
    ground_clearance_max: Optional[int] = None
    landing_height_min: Optional[int] = None
    landing_height_max: Optional[int] = None
    seats_min: Optional[int] = None
    seats_max: Optional[int] = None
    max_speed_min: Optional[int] = None
    max_speed_max: Optional[int] = None
    power_min: Optional[int] = None
    power_max: Optional[int] = None
    fuel_tank_capacity_min: Optional[int] = None
    fuel_tank_capacity_max: Optional[int] = None
    exist_navigator: Optional[bool] = None
    exist_compressor: Optional[bool] = None
    height_min: Optional[int] = None
    height_max: Optional[int] = None
    exist_headlight: Optional[bool] = None
    exist_turn_signal: Optional[bool] = None
    cylinder_number_min: Optional[int] = None
    cylinder_number_max: Optional[int] = None
    load_capacity_min: Optional[int] = None
    load_capacity_max: Optional[int] = None
    transmission: Optional[str] = None
    torque_min: Optional[int] = None
    torque_max: Optional[int] = None
    trunk_volume_min: Optional[int] = None
    trunk_volume_max: Optional[int] = None
    exist_radio_system: Optional[bool] = None

    approx_weight: Optional[WeightMeasure] = None

    limit: Optional[int] = None
