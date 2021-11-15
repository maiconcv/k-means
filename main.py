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
    dataset = Dataset(file_name, ' ', False)
    for i in range(2, 12):
        clusterizer = Clusterizer(i, dataset)
        clusterizer.run()
        exp = Exporter("benchmark" + "_" + str(i) + ".csv", dataset.INSTANCES, clusterizer.clusters)
        exp.export_to_file()


if __name__ == '__main__':
    main()