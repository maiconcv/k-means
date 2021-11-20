from cluster import Cluster
from typing import List, Dict
from dataset import Dataset
import utils
import random
import sys
import math


class Clusterizer(object):
    def __init__(self, k: int, dataset: Dataset, useKMeanspp: bool):
        self.k: int = k
        self.clusters: List[Cluster] = []
        self.USE_KMEANSPP = useKMeanspp
        # Dictionary of instance_id to cluster_id
        self.instance_dict: Dict[int, int] = {}
        self._DATASET: Dataset = dataset
        self._create_clusters()

    def _find_closest_cluster(self, instance_id: int) -> int:
        distances: List[float] = [utils.euclidean_distance(cluster.centroid, self._DATASET[instance_id]) for cluster in self.clusters]
        return distances.index(min(distances))

    def step(self) -> bool:
        '''
        Runs 1 step of the cluster.
        Returns if a cluster was changed or not.
        '''
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

    def run(self) -> float:
        '''
        Returns the WCSS value of the clusters.
        '''
        res = 0.0
        while self.step():
            res = self._wss()

        return res

    def _wss(self) -> float:
        result: float = 0.0
        for index in range(self.k):
            result += self.clusters[index].wss()
        return result

    def _generate_random_point(self) -> List[float]:
        return [random.uniform(0, 1) for _ in range(self._DATASET.NUM_ATTRIBUTES)]

    def _create_clusters(self) -> None:
        centroids: List[List[float]] = []
        centroids = self._initialize_centroids()
        self.clusters = [Cluster(self._DATASET, centroid) for centroid in centroids]

    def _initialize_centroids(self):
        '''
        K-Means++ initialization.
        For each cluster finds the data point furthest from the closest cluster.
        '''
        centroids = []
        if self.USE_KMEANSPP:
            centroids.append(random.choice(self._DATASET))
        
            for _ in range(self.k - 1):
                distances_to_closest_centroid = []
                for instance in self._DATASET:                
                    distance_to_closest_cluster = sys.maxsize
                    for centroid in centroids:
                        distance_to_centroid = utils.euclidean_distance(instance, centroid)
                        distance_to_closest_cluster = min(distance_to_closest_cluster, distance_to_centroid)
                    distances_to_closest_centroid.append(distance_to_closest_cluster)
                    
                index_furthest_point = distances_to_closest_centroid.index(max(distances_to_closest_centroid))
                next_centroid = self._DATASET[index_furthest_point]
                centroids.append(next_centroid)
                distances_to_closest_centroid = []
        else:
            centroids = random.choices(self._DATASET, k=self.k)

        return centroids