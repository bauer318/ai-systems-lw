from ranger import Ranger
from reader import get_dataset_array


class MeasureMain:
    items = get_dataset_array()
    measure_matrix_dict = None
    min_values: Ranger = None
