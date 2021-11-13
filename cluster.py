import statistics
import math

class Cluster(object):
    '''
    This class represents a cluster.
    '''
    def __init__(self, dataset):
        self._instances = []
        self._DATASET = dataset
        self.centroid = None

    def update_centroid(self) -> None:
        '''
        Updates the cluster's centroid based on the instances present on it.
        '''
        INSTANCES = [instance for idx, instance in enumerate(self._DATASET.instances) if idx in self._instances]
        NUM_ATTRIBUTES = len(instances[0])
        
        centroid_new_attributes = []
        for attr_idx in range(NUM_ATTRIBUTES):
            centroid_new_attributes.append(statistics.mean([r[attr_idx] for r in INSTANCES]))

        self.centroid = centroid_new_attributes

    def add_instance(self, instance_id: int) -> None:
        '''
        Adds a data instance reference (id on the dataset) to this cluster.
        '''
        self._instances.append(instance_id)

    def remove_instance(self, instance_id: int) -> None:
        '''
        Remove an instance from this cluster.
        '''
        self._instances.remove(instance_id)

    def distance(instance_id: int) -> float:
        '''
        Calculates the distance of an instance to this cluster's centroid.
        '''
        INSTANCE = self._DATASET[instance_id]
        assert len(INSTANCE) == len(self.centroid), 'Instance and Centroid must have the same number of attributes.'
        result = 0.0
        for x, y in zip(INSTANCE, self.centroid):
            result += (x - y) ** 2

        return math.sqrt(result)

    def __str__(self) -> str:
        return "Cluster with {0} instances".format(self._instances)

    def __repr__(self) -> str:
        return str(self)