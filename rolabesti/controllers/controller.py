from abc import ABC, abstractmethod

from rolabesti.conf.settings import DB
from rolabesti.database import MongoDB, TinyDB
from rolabesti.logger import Logger


class Controller(ABC):
    def __init__(self, parameters: dict) -> None:
        self.parameters = parameters
        match DB:
            case "mongo":
                self.db = MongoDB()
            case "tiny":
                self.db = TinyDB()
        self.logger = Logger()

    @abstractmethod
    def __call__(self) -> None:
        pass
