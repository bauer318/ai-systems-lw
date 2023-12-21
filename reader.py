from dataclass_csv import DataclassReader
import pandas as pd
from datasetitem import DatasetItem


def get_dataset_array():
    dataset = []
    with open("data/dataset.csv", "r") as csv_file:
        reader = DataclassReader(csv_file, DatasetItem, validate_header=False)
        for item in reader:
            dataset.append(item)
    return dataset

