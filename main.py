import csv
import sys
from typing import List

from data_instance import DataInstance


def get_file_name() -> str:
    try:
        return sys.argv[1]
    except IndexError:
        print('Missing dataset file argument. Exiting...')
        sys.exit()


def remove_spaces_of(line: List[str]) -> List[str]:
    return [element for element in line if element != '']


def read_dataset(file_name: str, delimiter: str) -> List[DataInstance]:
    data_instances = []

    try:
        with open(file_name) as data_file:
            lines = csv.reader(data_file, delimiter=delimiter)
            instance_index = 0
            for line in lines:
                attributes = remove_spaces_of(line)
                data_instances.append(DataInstance(instance_index, attributes))
                instance_index += 1
        return data_instances
    except FileNotFoundError:
        print('Dataset file not found. Exiting...')
        sys.exit()


def main():
    file_name = get_file_name()
    data_instances = read_dataset(file_name, delimiter=' ')
    print(data_instances)


if __name__ == '__main__':
    main()
