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