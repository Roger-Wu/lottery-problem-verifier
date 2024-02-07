from abc import ABC, abstractmethod
from typing import Iterable


class AbstractIntSet(ABC):
    """
    Abstract base class for sets that store only integers in in range(max_size).
    May use set, bitarray or numpy array to store data.
    """

    @abstractmethod
    def __init__(self, max_size: int, data: Iterable[int] = ()):
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def is_full(self) -> bool:
        pass

    @abstractmethod
    def add(self, item: int) -> None:
        pass

    @abstractmethod
    def union(self, another_set: "AbstractIntSet") -> "AbstractIntSet":
        pass

    @abstractmethod
    def update(self, another_set: "AbstractIntSet") -> None:
        pass

    @abstractmethod
    def difference(self, another_set: "AbstractIntSet") -> "AbstractIntSet":
        pass

    @abstractmethod
    def difference_update(self, another_set: "AbstractIntSet") -> None:
        pass
