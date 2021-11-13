from typing import List


class DataInstance:
    def __init__(self, instance_id: int, attributes: List[str]):
        self.id = instance_id
        self.attributes = attributes

    def __str__(self) -> str:
        return 'DataInstance{' \
               'id=' + str(self.id) + \
               ', attributes=' + str(self.attributes) + \
               '}'

    def __repr__(self) -> str:
        return str(self)
