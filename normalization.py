from typing import List, Tuple


def normalize_instances(dataset: List[List[str]]) -> List[List[float]]:
    attributes_quantity = len(dataset[0])
    attribute_min_max_values = __calculate_min_max_values_of_attributes(dataset)

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


def __calculate_min_max_values_of_attributes(dataset: List[List[str]]) -> List[Tuple[float, float]]:
    attributes_quantity = len(dataset[0])
    attribute_min_max_values = []
    for attr_index in range(attributes_quantity):
        min_value = min(map(lambda instance: float(instance[attr_index]), dataset))
        max_value = max(map(lambda instance: float(instance[attr_index]), dataset))
        attribute_min_max_values.append((min_value, max_value))
    return attribute_min_max_values
