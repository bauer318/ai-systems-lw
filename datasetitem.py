from dataclasses import dataclass


@dataclass
class DatasetItem:
    name: str
    brand: str
    weight: float
    engine_capacity: float
    color: str
    ground_clearance: str = ""
    landing_height: str = ""
    seats: str = ""
    max_speed: str = ""
    power: str = ""
    fuel_tank_capacity: str = ""
    exist_navigator: bool = False
    exist_compressor: bool = False
    height: str = ""
    exist_headlight: bool = False
    exist_turn_signal: bool = False
    cylinder_number: str = ""
    load_capacity: str = ""
    transmission: str = "Empty"
    torque: str = ""
    trunk_volume: str = ""
    exist_radio_system: bool = False
