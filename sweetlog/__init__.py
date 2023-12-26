"""SweetLog, pythonic logging package"""

__version__ = "0.1.1"

from .datatypes import LoggingLevel, Writable
from .logger import Logger
from .streams import FileLoggingStream
