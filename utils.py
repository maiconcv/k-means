from typing import List
import math
import csv


def euclidean_distance(p1, p2) -> float:
    """
    Calculates the distance of two given points.
    """
    assert len(p1) == len(p2), 'Points must have the same number of attributes.'
    result = 0.0
    for x, y in zip(p1, p2):
        result += (x - y) ** 2

    return math.sqrt(result)


def centroid_index(results: List[List[float]], ground_truth: List[List[float]]):
    """
    Calculates the centroid index.
    """
    nearest_map = {}
    for idx, res in enumerate(results):
        distances = [euclidean_distance(gt, res) for gt in ground_truth]
        nearest_map[idx] = distances.index(min(distances))    

    ci = 0
    for idx, _ in enumerate(ground_truth):
        orphan = True
        for k in nearest_map.keys():
            orphan = orphan and (nearest_map[k] != idx) 
        ci += 1 if orphan else 0

    return ci
    

def read_input_csv(file):
    raw_data_instances = []

    with open(file) as data_file:
        lines = csv.reader(data_file, delimiter='\t')
        header = next(lines)

        for line in lines:
            raw_data_instances.append(line)

    return raw_data_instances, header


def read_dataset_csv(file) -> List[List[str]]:
    """
    Reads the data from the dataset given.
    """
    raw_data_instances = []

    with open(file) as data_file:
        lines = csv.reader(data_file, delimiter=',')
        next(lines)

        for line in lines:
            #attributes = convert_line(line)
            raw_data_instances.append(line)

    return raw_data_instances