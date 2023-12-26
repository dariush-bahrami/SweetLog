import sys
from datetime import datetime
from functools import wraps
from inspect import signature
from typing import Callable, Iterable

from .datatypes import LoggingLevel, Writable


class Logger:
    def __init__(
        self,
        streams: Iterable[Writable] = [sys.stdout],
        level=LoggingLevel.WARNING,
    ):
        self.streams = streams
        self.level = level

    def __repr__(self):
        return f"Logger(stream={self.stream}, level={self.level})"

    def write(self, message: str, level: LoggingLevel):
        if level.value >= self.level.value:
            datetime_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            level_string = level.name
            for stream in self.streams:
                stream.write(f"[{datetime_string}] [{level_string}] {message}\n")
                stream.flush()

    def debug(self, message):
        self.write(message, LoggingLevel.DEBUG)

    def info(self, message):
        self.write(message, LoggingLevel.INFO)

    def warning(self, message):
        self.write(message, LoggingLevel.WARNING)

    def error(self, message):
        self.write(message, LoggingLevel.ERROR)

    def critical(self, message):
        self.write(message, LoggingLevel.CRITICAL)

    def get_decorator(
        self,
        level=LoggingLevel.DEBUG,
        log_arguments=True,
        log_return=True,
    ) -> Callable:
        def decorator(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                message_parts = ["Calling"]
                if log_arguments is True:
                    arguments = signature(function).bind(*args, **kwargs).arguments
                    arguments_string = ", ".join(
                        [f"{key}={value}" for key, value in arguments.items()]
                    )
                    message_parts.append(f"{function.__name__}({arguments_string})")

                else:
                    message_parts.append(function.__name__)

                if log_return is True:
                    result = function(*args, **kwargs)
                    message_parts.append(f"-> {result}")
                    message = " ".join(message_parts)
                    self.write(message, level)
                    return result

                else:
                    message = " ".join(message_parts)
                    self.write(message, level)
                    return function(*args, **kwargs)

            return wrapper

        return decorator
