import csv
import sys
from pathlib import Path
from typing import List, Tuple
from constants import TYPE_MAP


class Dataset(object):
    """
    This class represents the dataset.
    """

    def __init__(self, filename: str, delimiter: str, has_header: bool, ground_truth: bool = None):
        self._FILENAME = filename
        self._DELIMITER = delimiter
        self._HAS_HEADER = has_header
        self._METADATA = self._read_metadata()
        self._RAW_INSTANCES: List[List[str]] = self._read_dataset()
        self.NUM_INSTANCES: int = len(self._RAW_INSTANCES)
        self.NUM_ATTRIBUTES_RAW: int = len(self._RAW_INSTANCES[0])
        self._HOT_ENCODING, self._METADATA = self._one_hot_encoding()
        self.NUM_ATTRIBUTES: int = len(self._HOT_ENCODING[0])
        self.INSTANCES = self._normalize_instances()
        self.GROUND_TRUTH = self._read_ground_truth_file() if ground_truth else None

    def _remove_spaces_of(self, line: List[str]) -> List[str]:
        return [element for element in line if element != '']

    def _read_dataset(self) -> List[List[str]]:
        """
        Reads the data from the dataset given.
        """
        raw_data_instances = []

        try:
            with open(self._FILENAME) as data_file:
                lines = csv.reader(data_file, delimiter=self._DELIMITER if self._DELIMITER != "tab" else '\t')
                if self._HAS_HEADER:
                    next(lines)

                for line in lines:
                    attributes = self._remove_spaces_of(line)
                    raw_data_instances.append(attributes)

            return raw_data_instances
        except FileNotFoundError:
            print('Dataset file not found. Exiting...')
            sys.exit()

    def _one_hot_encoding(self) -> List[List[float]]:
        hot_dataset = []
        uniques = {}
        new_metadata = []
        for index, meta in enumerate(self._METADATA):
            if meta == 'c':
                column = map(lambda instance: instance[index], self._RAW_INSTANCES)
                uniques[index] = sorted(list(set(column)))
                for _ in uniques[index]:
                    new_metadata.append('b')
            else:
                new_metadata.append(meta)

        for instance in self._RAW_INSTANCES:
            new_instance = []
            for index, meta in enumerate(self._METADATA):
                if meta == 'c':
                    for unique in uniques[index]:
                        if instance[index] == unique:
                            new_instance.append(1.0)
                        else:
                            new_instance.append(0.0)
                else:
                    new_instance.append(instance[index])
            hot_dataset.append(new_instance)
        return hot_dataset, new_metadata

    def _normalize_instances(self) -> List[List[float]]:
        attribute_min_max_values = self._calculate_min_max_values_of_attributes()

        normalized_dataset = []
        for instance_index in range(self.NUM_INSTANCES):
            parsed_instance = self._parse_attributes(self._HOT_ENCODING[instance_index])
            normalized_instance = []
            for attr_index in range(self.NUM_ATTRIBUTES):
                min_value, max_value = attribute_min_max_values[attr_index]
                instance_attribute_value = parsed_instance[attr_index]

                normalized_attribute = (instance_attribute_value - min_value) / (max_value - min_value)
                normalized_instance.append(normalized_attribute)
            normalized_dataset.append(normalized_instance)

        return normalized_dataset

    def _calculate_min_max_values_of_attributes(self) -> List[Tuple[float, float]]:
        attribute_min_max_values = []
        for attr_index in range(self.NUM_ATTRIBUTES):
            min_value = min(map(lambda instance: float(instance[attr_index]), self._HOT_ENCODING))
            max_value = max(map(lambda instance: float(instance[attr_index]), self._HOT_ENCODING))
            attribute_min_max_values.append((min_value, max_value))

        return attribute_min_max_values

    def _read_metadata(self) -> List[str]:
        """
        Reads the metadata file associated with data.
        Metadata files are files with only one csv line.
        It is expected that metadata file names are just the db file name with _metadata appended to it.
        """
        try:
            p = Path(self._FILENAME)
            p = p.with_name(p.stem + "_metadata.csv")
            with open(p) as f:
                reader = csv.reader(f, delimiter=",")
                metadata = next(reader)

            return metadata
        except FileNotFoundError:
            print("Dataset metadata file not found. Exiting...")
            sys.exit()

    def _parse_attributes(self, raw_attributes: List[str]) -> List[float]:
        """
        Parses attributes according to their type and return a numerical value.
        """
        assert len(raw_attributes) == len(self._METADATA), "Mismatch in the metadata and attributes read."

        return [TYPE_MAP[self._METADATA[idx]](attribute) for idx, attribute in enumerate(raw_attributes)]

    def _read_ground_truth_file(self):
        ground_truth = []
        raw_data_instances = []

        p = Path(self._FILENAME)
        p = p.with_name(p.stem + "_groundtruth.txt")
        with open(p) as data_file:
            lines = csv.reader(data_file, delimiter=self._DELIMITER)
            if self._HAS_HEADER:
                next(lines)

            for line in lines:
                attributes = self._remove_spaces_of(line)
                raw_data_instances.append(attributes)

        attribute_min_max_values = self._calculate_min_max_values_of_attributes()

        for gt_idx in range(len(raw_data_instances)):
            parsed_instance = self._parse_attributes(raw_data_instances[gt_idx])
            normalized_instance = []
            for attr_index in range(self.NUM_ATTRIBUTES):
                min_value, max_value = attribute_min_max_values[attr_index]
                instance_attribute_value = parsed_instance[attr_index]

                normalized_attribute = (instance_attribute_value - min_value) / (max_value - min_value)
                normalized_instance.append(normalized_attribute)
            ground_truth.append(normalized_instance)

        return ground_truth

    def __getitem__(self, key):
        return self.INSTANCES[key]

    def __iter__(self):
        return self.INSTANCES.__iter__()

    def __next__(self):
        return next(self.INSTANCES)

    def __len__(self):
        return len(self.INSTANCES)

    def __str__(self):
        return "Dataset with {0} instances and {1} attributes".format(self.NUM_INSTANCES, self.NUM_ATTRIBUTES)

    def __repr__(self):
        return str(self)
