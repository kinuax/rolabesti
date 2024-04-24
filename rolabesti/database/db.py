from abc import ABC, abstractmethod
from collections.abc import Generator
from pathlib import Path


class DB(ABC):
    @abstractmethod
    def count(self) -> int:
        pass

    @abstractmethod
    def empty(self) -> None:
        pass

    @abstractmethod
    def insert_one(self, track: dict) -> None:
        pass

    @abstractmethod
    def search(self, search_filters: dict) -> Generator[dict, None, None]:
        pass

    @abstractmethod
    def update_one(self, path: Path, field: str, value: str | int) -> None:
        pass
