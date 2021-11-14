import csv
import sys
from typing import List, Tuple

from data_instance import DataInstance


class Dataset(object):
    '''
    This class represents the dataset.
    '''

    def __init__(self, filename: str):
        self.NUM_INSTANCES: int = 0
        self.NUM_ATTRIBUTES: int = 0
        self.instances = self._read_dataset(filename, delimiter=' ')

    def __getitem__(self, key):
        return self.instances[key]

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.instances)

    def _remove_spaces_of(self, line: List[str]) -> List[str]:
        return [element for element in line if element != '']

    def _read_dataset(self, file_name: str, delimiter: str) -> List[DataInstance]:
        data_instances = []
        try:
            with open(file_name) as data_file:
                lines = csv.reader(data_file, delimiter=delimiter)
                instance_index = 0
                for line in lines:
                    attributes = self._remove_spaces_of(line)
                    data_instances.append(DataInstance(instance_index, attributes))
                    instance_index += 1
            return data_instances
        except FileNotFoundError:
            print('Dataset file not found. Exiting...')
            sys.exit()

    def _normalize_instances(self, dataset: List[List[str]]) -> List[List[float]]:
        attributes_quantity = len(dataset[0])
        attribute_min_max_values = self._calculate_min_max_values_of_attributes(dataset)

        normalized_dataset = []
        for instance_index in range(len(dataset)):
            normalized_instance = []
            for attr_index in range(attributes_quantity):
                min_value, max_value = attribute_min_max_values[attr_index]
                instance_attribute_value = float(dataset[instance_index][attr_index])

                normalized_attribute = (instance_attribute_value - min_value) / (max_value - min_value)
                normalized_instance.append(normalized_attribute)
            normalized_dataset.append(normalized_instance)

        return normalized_dataset

    def _calculate_min_max_values_of_attributes(self, dataset: List[List[str]]) -> List[Tuple[float, float]]:
        attributes_quantity = len(dataset[0])
        attribute_min_max_values = []
        for attr_index in range(attributes_quantity):
            min_value = min(map(lambda instance: float(instance[attr_index]), dataset))
            max_value = max(map(lambda instance: float(instance[attr_index]), dataset))
            attribute_min_max_values.append((min_value, max_value))
        return attribute_min_max_values
