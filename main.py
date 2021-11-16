import sys
from dataset import Dataset
from clusterizer import Clusterizer
from exporter import Exporter


def get_file_name() -> str:
    try:
        return sys.argv[1]
    except IndexError:
        print('Missing dataset file argument. Exiting...')
        sys.exit()


def main():
    file_name = get_file_name()
    dataset = Dataset(file_name, ' ', False, True)

    wss_values = []
    for i in range(15, 16):
        print("Running K-Means with {0} clusters...".format(i))
        clusterizer = Clusterizer(i, dataset)
        wss_values.append([i, clusterizer.run()])
        exp = Exporter("benchmark" + "_" + str(i) + ".csv", dataset.INSTANCES, clusterizer.clusters, dataset.GROUND_TRUTH)
        exp.export_to_file()

    exp = Exporter("WCSS_Values.csv", wss=wss_values)
    exp.export_to_file()


if __name__ == '__main__':
    main()
