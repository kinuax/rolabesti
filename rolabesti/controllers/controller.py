from abc import ABC, abstractmethod

from rolabesti.database import MongoDB
from rolabesti.logger import Logger


class Controller(ABC):
    def __init__(self, parameters: dict) -> None:
        self.parameters = parameters
        self.db = MongoDB()
        self.logger = Logger()

    @abstractmethod
    def __call__(self) -> None:
        pass
