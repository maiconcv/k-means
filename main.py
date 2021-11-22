import argparse
import statistics
from pathlib import Path
from dataset import Dataset
from clusterizer import Clusterizer
from exporter import Exporter
from utils import *


def main(args):
    p = Path(args.d)
    dataset = Dataset(args.d, args.s, args.header, args.gt)

    wss_values = []
    
    ci_total = 0
    for i in range(args.k_base if (args.k_base is not None) else args.k, args.k + 1):
        print("Running K-Means with {0} clusters...".format(i))
        clusterizer = Clusterizer(i, dataset, args.kmeanspp)
        wss_values.append((i, clusterizer.run()))
        exp = Exporter(p.stem + "_" + str(i) + "_" + str(args.kmeanspp) + ".csv", dataset.INSTANCES, clusterizer.clusters, dataset.GROUND_TRUTH)
        
        if dataset.GROUND_TRUTH is not None:
            ci_value = centroid_index([c.centroid for c in clusterizer.clusters], dataset.GROUND_TRUTH)
            ci_total += ci_value
            print("Centroid index: {}".format(ci_value))
            exp.export_to_file()
        else:
            exp.export_results()

    exp = Exporter(p.stem + "_WCSS_Values.csv", wss=wss_values)
    exp.export_to_file()


def run_centroid_index(args):
    p = Path(args.d)
    dataset = Dataset(args.d, args.s, args.header, args.gt)

    ci_values = ["Centroid Index"]
    for i in range(100):
        print("Running K-Means with {0} clusters... {1}/100".format(args.k, i))
        clusterizer = Clusterizer(args.k, dataset, args.kmeanspp)
        clusterizer.run()
        
        if dataset.GROUND_TRUTH is not None:
            ci_value = centroid_index([c.centroid for c in clusterizer.clusters], dataset.GROUND_TRUTH)
            ci_values.append([ci_value])
            print("Centroid index: {}".format(ci_value))

    exp = Exporter(p.stem + "_CI_Values.csv", ci=ci_values)
    exp.export_ci_values()


def get_personas():
    DATASET_PATH = "./results/bank_t2_5_True.csv"
    INPUT_PATH = "./dataset/bank_t2.txt"
    DATA_ID_COL = 0
    CLUSTER_ID_COL = 1

    dataset = read_dataset_csv(DATASET_PATH)
    input, header = read_input_csv(INPUT_PATH)

    splitted_clusters = {}
    for data in dataset:
        if data[CLUSTER_ID_COL] not in splitted_clusters.keys():
            splitted_clusters[data[CLUSTER_ID_COL]] = [data[DATA_ID_COL]]
        else:
            splitted_clusters[data[CLUSTER_ID_COL]].append(data[DATA_ID_COL])

    print(splitted_clusters.keys())

    print("Cluster personas:")
    for k in splitted_clusters.keys():
        raw_data = [input[int(data)] for data in splitted_clusters[k]]
        print("\tCluster {0}".format(k))
        # Retrieve all values from column
        for attr_id in range(len(input[0])):
            values = [data[attr_id] for data in raw_data]
            attr_mode = statistics.mode(values)
            print("\t\tAttribute '{0}': {1}".format(header[attr_id], attr_mode))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs K-Means clustering.')
    parser.add_argument('-d', type=str, help='path to the dataset file', metavar="dataset", required=True)
    parser.add_argument('-s', type=str, help='dataset file delimiter (use "tab" in lowercase for \\t)', metavar='separator', required=True)
    parser.add_argument('-k', type=int, help='value for the hyperparameter k', required=True)
    parser.add_argument('-k_base', type=int, nargs='?', default=None, help='lower range value for k')
    parser.add_argument('-header', action='store_true', help='if the dataset file has a header')
    parser.add_argument('-gt', action='store_true', help='if the dataset file has a corresponding ground truth file')
    parser.add_argument('-kmeanspp', action='store_true', help='if the kmeans++ initialization should be used by the clusterizer')
    parser.add_argument('-ci_experiment', action='store_true', help='if the centroid index experiment should be run. Requires k, dataset, ground truth and separator.')
    parser.add_argument('-personas', action='store_true', help='get personas from the results.')

    args = parser.parse_args()
    if (args.ci_experiment):
        run_centroid_index(args)
    elif (args.personas):
        get_personas()
    else:
        main(args)