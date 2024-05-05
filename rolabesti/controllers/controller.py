import os
from abc import ABC, abstractmethod

from rolabesti.config import get_settings, tinydb_directory, tinydb_file
from rolabesti.database import TinyDB
from rolabesti.logger import Logger


settings = get_settings()


class Controller(ABC):
    def __init__(self, parameters: dict) -> None:
        self.parameters = parameters
        match settings.database:
            case "tinydb":
                if not tinydb_directory.exists():
                    os.mkdir(tinydb_directory)
                self.db = TinyDB(tinydb_file)
        self.logger = Logger()

    @abstractmethod
    def __call__(self) -> None:
        pass
