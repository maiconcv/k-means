import sys
from dataset import Dataset
from clusterizer import Clusterizer


def get_file_name() -> str:
    try:
        return sys.argv[1]
    except IndexError:
        print('Missing dataset file argument. Exiting...')
        sys.exit()


def main():
    file_name = get_file_name()
    dataset = Dataset(file_name, ' ', False)
    clusterizer = Clusterizer(5, dataset)
    clusterizer.run()


if __name__ == '__main__':
    main()