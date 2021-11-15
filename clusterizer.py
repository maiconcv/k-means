from cluster import Cluster
from typing import List, Dict
from dataset import Dataset
import random


class Clusterizer(object):
    def __init__(self, k: int, dataset: Dataset):
        self.k: int = k
        self.clusters: List[Cluster] = []
        # Dictionary of instance_id to cluster_id
        self.instance_dict: Dict[int, int] = {}
        self._DATASET: Dataset = dataset
        self._create_clusters()

    def _find_closest_cluster(self, instance_id: int) -> int:
        distances: List[float] = [cluster.distance(instance_id) for cluster in self.clusters]
        return distances.index(min(distances))

    def step(self) -> bool:
        changed = False
        if len(self.instance_dict) == 0:
            changed = True
            for instance_id in range(self._DATASET.NUM_INSTANCES):
                cluster_id = self._find_closest_cluster(instance_id)
                self.clusters[cluster_id].add_instance(instance_id)
                self.instance_dict[instance_id] = cluster_id
        else:
            for instance_id in range(self._DATASET.NUM_INSTANCES):
                cluster_id = self._find_closest_cluster(instance_id)
                old_cluster_id = self.instance_dict[instance_id]
                if old_cluster_id != cluster_id:
                    changed = True
                    self.clusters[old_cluster_id].remove_instance(instance_id)
                    self.clusters[cluster_id].add_instance(instance_id)
                    self.instance_dict[instance_id] = cluster_id
        if changed:
            for cluster in self.clusters:
                cluster.update_centroid()

        return changed

    def run(self):
        while self.step():
            print(self.wss())

    def wss(self):
        result: float = 0.0
        for index in range(self.k):
            result += self.clusters[index].wss()
        return result

    def _generate_random_point(self):
        return [random.uniform(0, 1) for _ in range(self._DATASET.NUM_ATTRIBUTES)]

    def _create_clusters(self):
        centroids: List[float] = []
        for _ in range(self.k):
            cluster: Cluster = Cluster(self._DATASET)
            candidate = self._generate_random_point()
            while candidate in centroids:
                candidate = self._generate_random_point()
            centroids.append(candidate)
            cluster.centroid = candidate
            self.clusters.append(cluster)
