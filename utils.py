from typing import List
import math


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
    '''
    Calculates the centroid index.
    '''
    nearest_map = {}
    for idx, res in enumerate(results):
        distances = [euclidean_distance(gt, res.centroid) for gt in ground_truth]
        nearest_map[idx] = distances.index(min(distances))    

    ci = 0
    for idx, _ in enumerate(ground_truth):
        orphan = True
        for k in nearest_map.keys():
            orphan = orphan and (nearest_map[k] != idx) 
        ci += 1 if orphan else 0

    return ci