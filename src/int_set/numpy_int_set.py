import numpy as np
from typing import Iterable
from abstract_int_set import AbstractIntSet


class NumpyIntSet(AbstractIntSet):
    """
    Use Numpy array as a set that stores only integers in range(max_size).
    """
    def __init__(self, max_size: int, data: Iterable[int] = ()):
        self.array = np.zeros(max_size, dtype=bool)
        for item in data:
            self.array[item] = True
        self.max_size = max_size

    def __len__(self) -> int:
        return np.sum(self.array)

    def __bool__(self):
        """Return False if the set is empty, True otherwise"""
        return not np.any(self.array)

    def __sub__(self, another_set):
        return self.difference(another_set)

    def __and__(self, another_set):
        return self.intersection(another_set)

    def __or__(self, another_set):
        return self.union(another_set)

    def is_full(self) -> bool:
        return np.all(self.array)

    def add(self, item: int) -> None:
        self.array[item] = True

    def union(self, another_set: 'NumpyIntSet') -> 'NumpyIntSet':
        result_set = NumpyIntSet(self.max_size)
        result_set.array = np.bitwise_or(self.array, another_set.array)
        return result_set

    def update(self, another_set: 'NumpyIntSet') -> None:
        self.array = np.bitwise_or(self.array, another_set.array)

    def difference(self, another_set: 'NumpyIntSet') -> 'NumpyIntSet':
        result_set = NumpyIntSet(self.max_size)
        result_set.array = np.bitwise_and(self.array, np.bitwise_not(another_set.array))
        return result_set

    def difference_update(self, another_set: 'NumpyIntSet') -> None:
        self.array = np.bitwise_and(self.array, np.bitwise_not(another_set.array))

    def intersection(self, another_set: "NumpyIntSet") -> "NumpyIntSet":
        result_set = NumpyIntSet(self.max_size)
        result_set.array = np.bitwise_and(self.array, another_set.array)
        return result_set

    def intersection_update(self, another_set: "NumpyIntSet") -> None:
        self.array = np.bitwise_and(self.array, another_set.array)
