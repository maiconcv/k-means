import sys
import argparse
from pathlib import Path
from dataset import Dataset
from clusterizer import Clusterizer
from exporter import Exporter
from utils import *


def main(args):
    p = Path(args.d)
    dataset = Dataset(args.d, args.s, args.header, args.gt)

    wss_values = []
    
    for i in range(args.k_base if (args.k_base is not None) else args.k, args.k + 1):
        print("Running K-Means with {0} clusters...".format(i))
        clusterizer = Clusterizer(i, dataset, args.kmeanspp)
        wss_values.append([i, clusterizer.run()])
        exp = Exporter(p.stem + "_" + str(i) + "_" + str(args.kmeanspp) + ".csv", dataset.INSTANCES, clusterizer.clusters, dataset.GROUND_TRUTH)
        exp.export_to_file()
        
        if dataset.GROUND_TRUTH is not None:
            print("Centroid index: {}".format(centroid_index([c.centroid for c in clusterizer.clusters], dataset.GROUND_TRUTH)))

    exp = Exporter(p.stem + "_WCSS_Values.csv", wss=wss_values)
    exp.export_to_file()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs K-Means clustering.')
    parser.add_argument('-k', type=int, help='value for the hyperparameter k')
    parser.add_argument('-k_base', type=int, nargs='?', default=None, help='lower range value for k')
    parser.add_argument('-d', type=str, help='path to the dataset file')
    parser.add_argument('-s', type=str, help='dataset file delimiter')
    parser.add_argument('-header', action='store_true', help='if the dataset file has a header')
    parser.add_argument('-gt', action='store_true', help='if the dataset file has a corresponding ground truth file')
    parser.add_argument('-kmeanspp', action='store_true', help='if the kmeans++ initialization should be used by the clusterizer')

    args = parser.parse_args()
    main(args)