from abc import ABC, abstractmethod
from enum import Enum


class Writable(ABC):
    @abstractmethod
    def write(self, message):
        ...

    @abstractmethod
    def flush(self):
        ...


class LoggingLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
