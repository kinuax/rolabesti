from abc import ABCMeta, abstractmethod
from collections.abc import Generator
from pathlib import Path

from docstring_inheritance import NumpyDocstringInheritanceMeta


# Support docstring inheritance.
class ABCNumpyDocstringInheritanceMeta(ABCMeta, NumpyDocstringInheritanceMeta):
    pass


class DB(metaclass=ABCNumpyDocstringInheritanceMeta):
    @abstractmethod
    def count(self) -> int:
        """Return the number of tracks."""
        pass

    @abstractmethod
    def empty(self) -> None:
        """Delete all tracks."""
        pass

    @abstractmethod
    def insert_many(self, tracks: list[dict]) -> None:
        """Insert multiple tracks."""
        pass

    @abstractmethod
    def search(self, search_filters: dict) -> Generator[dict, None, None]:
        """Return an iterator of matching tracks based on the search filters."""
        pass

    @abstractmethod
    def update_one(self, path: Path, field: str, value: str | int) -> None:
        """Update one field in one track."""
        pass
