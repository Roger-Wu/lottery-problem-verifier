from typing import Iterable, List, Set
from abstract_int_set import AbstractIntSet


class NativeIntSet(AbstractIntSet):
    """
    A native set implementation that stores only integers in range(max_size).
    """

    def __init__(
        self,
        max_size: int,
        data: Iterable[int] = (),
    ):
        self.max_size = max_size
        self.data = set(data)
        # for item in self.data:
        #     self._validate_item(item)

    def _validate_item(self, item: int) -> None:
        if not (0 <= item < self.max_size):
            raise ValueError("item must be in range(0, max_size).")

    def __len__(self) -> int:
        return len(self.data)

    def __bool__(self):
        """Return False if the set is empty, True otherwise"""
        return bool(self.data)

    def __sub__(self, another_set):
        return self.difference(another_set)

    def __and__(self, another_set):
        return self.intersection(another_set)

    def __or__(self, another_set):
        return self.union(another_set)

    def __iter__(self):
        # Return an iterator over the items in the set
        return iter(self.data)

    def is_full(self) -> bool:
        return len(self.data) == self.max_size

    def get_items(self) -> Set[int]:
        return set(self.data)

    def add(self, item: int) -> None:
        # self._validate_item(item)
        self.data.add(item)

    def union(self, another_set: "NativeIntSet") -> "NativeIntSet":
        result_set = NativeIntSet(self.max_size)
        result_set.data = self.data | another_set.data
        return result_set

    def update(self, another_set: "NativeIntSet") -> None:
        self.data.update(another_set.data)

    def difference(self, another_set: "NativeIntSet") -> "NativeIntSet":
        result_set = NativeIntSet(self.max_size)
        result_set.data = self.data.difference(another_set.data)
        return result_set

    def difference_update(self, another_set: "NativeIntSet") -> None:
        self.data.difference_update(another_set.data)

    def intersection(self, another_set: "NativeIntSet") -> "NativeIntSet":
        result_set = NativeIntSet(self.max_size)
        result_set.data = self.data.intersection(another_set.data)
        return result_set

    def intersection_update(self, another_set: "NativeIntSet") -> None:
        self.data.intersection_update(another_set.data)

    def negation(self) -> "NativeIntSet":
        """
        Return a new set that contains all the items not in this set.
        """
        result_set = NativeIntSet(self.max_size)
        result_set.data = set(range(self.max_size)) - self.data
        return result_set

    def negation_update(self) -> None:
        self.data = set(range(self.max_size)) - self.data
