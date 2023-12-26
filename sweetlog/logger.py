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
        level: LoggingLevel = LoggingLevel.WARNING,
        datettime_format: str = "%Y-%m-%d %H:%M:%S",
        logging_format: str = "[{datetime_string}] [{level_string}] {message}",
    ) -> None:
        self.streams = streams
        self.level = level
        self.datettime_format = datettime_format
        self.logging_format = logging_format

    def __repr__(self) -> str:
        return f"Logger(streams={self.streams}, level={self.level})"

    def write(self, message: str, level: LoggingLevel) -> None:
        if level.value >= self.level.value:
            datetime_string = datetime.now().strftime(self.datettime_format)
            level_string = level.name
            formatted_message = (
                self.logging_format.format(
                    datetime_string=datetime_string,
                    level_string=level_string,
                    message=message,
                )
                + "\n"
            )
            for stream in self.streams:
                stream.write(formatted_message)
                stream.flush()

    def debug(self, message: str) -> None:
        self.write(message, LoggingLevel.DEBUG)

    def info(self, message: str) -> None:
        self.write(message, LoggingLevel.INFO)

    def warning(self, message: str) -> None:
        self.write(message, LoggingLevel.WARNING)

    def error(self, message: str) -> None:
        self.write(message, LoggingLevel.ERROR)

    def critical(self, message: str) -> None:
        self.write(message, LoggingLevel.CRITICAL)

    def get_decorator(
        self,
        level: LoggingLevel = LoggingLevel.DEBUG,
        log_arguments: bool = True,
        log_return: bool = True,
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
