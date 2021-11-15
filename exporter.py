import os
import csv
from typing import List

from cluster import Cluster


class Exporter(object):
    """
    Exports cluster results.
    """
    def __init__(self, target_file: str, data: List[List[float]], clusters: List[Cluster]):
        self.FILENAME = target_file
        self.CLUSTERS: List[Cluster] = clusters
        self.DATA = data

    def export_to_file(self):
        if not os.path.exists('./results'):
            os.mkdir('./results/')
        
        csv_rows = [['x', 'Data', 'Cluster']]

        for data in self.DATA:
            csv_rows.append([str(data[0]), str(data[1]), ''])

        for cluster_res in self.CLUSTERS:
            csv_rows.append([str(cluster_res.centroid[0]), '', str(cluster_res.centroid[1])])

        with open("./results/" + self.FILENAME, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(csv_rows)
