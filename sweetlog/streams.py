from pathlib import Path

from .datatypes import Writable


class FileLoggingStream(Writable):
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def write(self, message: str) -> None:
        with open(self.file_path, "a+") as f:
            f.write(message)

    def flush(self) -> None:
        pass
