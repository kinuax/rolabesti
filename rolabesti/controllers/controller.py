from abc import ABC, abstractmethod

from rolabesti.config import get_settings, tinydb_file
from rolabesti.database import TinyDB
from rolabesti.logger import Logger


settings = get_settings()


class Controller(ABC):
    def __init__(self, parameters: dict) -> None:
        self.parameters = parameters
        match settings.database:
            case "tinydb":
                self.db = TinyDB(tinydb_file)
        self.logger = Logger()

    @abstractmethod
    def __call__(self) -> None:
        pass
