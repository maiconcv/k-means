import statistics
import math
from dataset import Dataset
from typing import List


class Cluster(object):
    """
    This class represents a cluster.
    """

    def __init__(self, dataset: Dataset, centroid: List[float]):
        self._instances = []
        self._DATASET: Dataset = dataset
        self.centroid = centroid

    def update_centroid(self) -> None:
        """
        Updates the cluster's centroid based on the instances present on it.
        """
        instances = [instance for idx, instance in enumerate(self._DATASET) if idx in self._instances]

        centroid_new_attributes = []
        if len(instances) == 0:
            # Não seria melhor randomizar?
            centroid_new_attributes = [0 for _ in range(self._DATASET.NUM_ATTRIBUTES)]
            print("Cluster with no data inside!")
        else:
            for attr_idx in range(self._DATASET.NUM_ATTRIBUTES):
                centroid_new_attributes.append(statistics.mean([r[attr_idx] for r in instances]))

        self.centroid = centroid_new_attributes

    def add_instance(self, instance_id: int) -> None:
        """
        Adds a data instance reference (id on the dataset) to this cluster.
        """
        if instance_id not in self._instances:
            self._instances.append(instance_id)

    def remove_instance(self, instance_id: int) -> None:
        """
        Remove an instance from this cluster.
        """
        self._instances.remove(instance_id)

    def wss(self) -> float:
        result: float = 0.0
        INSTANCES = [instance for idx, instance in enumerate(self._DATASET) if idx in self._instances]
        for INSTANCE in INSTANCES:
            for x, y in zip(INSTANCE, self.centroid):
                result += (x - y) ** 2
        return result

    def __str__(self) -> str:
        return "Cluster with {0} instances".format(self._instances)

    def __repr__(self) -> str:
        return str(self)
