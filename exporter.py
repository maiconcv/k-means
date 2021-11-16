import os
import csv
from typing import List, Tuple
from cluster import Cluster


class Exporter(object):
    """
    Exports cluster results.
    """
    def __init__(self, target_file: str, data: List[List[float]] = None, clusters: List[Cluster] = None, ground_truth: List[List[float]] = None, wss: List[Tuple[int, float]] = None):
        self.FILENAME = target_file
        self.CLUSTERS: List[Cluster] = clusters
        self.DATA = data
        self.GROUND_TRUTH = ground_truth
        self.WCSS = wss
    
    def export_to_file(self):
        if not os.path.exists('./results'):
            os.mkdir('./results/')

        if self.WCSS is None:
            csv_rows = [['x', 'Data', 'Cluster', 'Ground Truth']]

            for data in self.DATA:
                csv_rows.append([str(data[0]), str(data[1]), '', ''])

            for cluster_res in self.CLUSTERS:
                csv_rows.append([str(cluster_res.centroid[0]), '', str(cluster_res.centroid[1]), ''])

            for gt in self.GROUND_TRUTH:
                csv_rows.append([str(gt[0]), '', '', str(gt[1])])

            with open("./results/" + self.FILENAME, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(csv_rows)
        else:
            csv_rows = [['K', 'WCSS']]

            for data in self.WCSS:
                csv_rows.append(data)

            with open("./results/" + self.FILENAME, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(csv_rows)