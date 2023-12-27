# SweetLog

<div align="center">
<img src="https://raw.githubusercontent.com/dariush-bahrami/SweetLog/main/assets/sweetlog.png" alt="SweetLog Logo" width="256" st/>
</div>

<p align="center">
<i>SweetLog, pythonic logging package</i>
</p>

<div align="center">
<a href="https://pypi.org/project/sweetlog/">
<img src="https://badge.fury.io/py/sweetlog.svg" alt="SweetLog Logo" width="128" st/>
</a>
</div>

<br>

**SweetLog** is a Python logging package that provides a simple and flexible way to handle logging in your applications. It includes several components that you can use to customize your logging behavior.

## Installation

You can install SweetLog using `pip`:

```bash
pip install sweetlog
```

or just clone the repository:

```bash
git clone https://github.com/dariush-bahrami/SweetLog.git
```

there is no dependencies, so you can just copy the `sweetlog` folder to your project.

## Usage

You can use the `Logger` class to create a logger and log messages. You can also use the `FileLoggingStream` class to log messages to a file. Here is an example:

```python
from pathlib import Path
from sweetlog import Logger, FileLoggingStream, LoggingLevel

# Create a FileLoggingStream
file_stream = FileLoggingStream(Path('log.txt'))

# Create a logger with the file stream and level set to DEBUG
logger = Logger([file_stream], level=LoggingLevel.DEBUG)

# Log a debug message
logger.debug('This is a debug message')
```

This will write the debug message to the `log.txt` file. If you want to add `stdout` as a stream, you can do this:

```python
import sys
from pathlib import Path
from sweetlog import Logger, FileLoggingStream, LoggingLevel

# Create a FileLoggingStream
file_stream = FileLoggingStream(Path('log.txt'))

# Create a logger with the file and stdout streams and level set to DEBUG
logger = Logger([file_stream, sys.stdout], level=LoggingLevel.DEBUG)

# Log a debug message
logger.debug('This is a debug message')
```

This will write the debug message to the `log.txt` file and to the console.

`Logger` also has a `get_decorator` method that returns a decorator that can be used to log function calls. Here is an example:

```python
from pathlib import Path
from sweetlog import Logger, FileLoggingStream, LoggingLevel

# Create a FileLoggingStream
file_stream = FileLoggingStream(Path('log.txt'))

# Create a logger with the file stream and level set to DEBUG
logger = Logger([file_stream], level=LoggingLevel.DEBUG)

# Create a decorator that logs function calls
decorator = logger.get_decorator(
    level=LoggingLevel.DEBUG,
    log_arguments=True,
    log_return=True,
)

@decorator
def example_function(a, b):
    return a + b

example_function(1, 2)
```

This will write the following to the `log.txt` file:

`Calling example_function(a=1, b=2) -> 3`

## Components

### `LoggingLevel`

This is an enumeration in the `datatypes.py` file that defines the different levels of logging. The levels are DEBUG, INFO, WARNING, ERROR, and CRITICAL. Each level has a specific value, and the logger will only log messages with a level that is equal to or higher than its own level.

### `Writable`

This is an interface defined in the `datatypes.py` file. It represents a writable stream and has a `write` method that takes a string and writes it to the stream. It also has a `flush` method that flushes the stream.

### `Logger`

This is a class defined in the `logger.py` file. It is the main component of the SweetLog package. It takes a list of `Writable` streams and a `LoggingLevel` as input. It has methods for logging messages at each level (debug, info, warning, error, critical). It also has a `write` method that writes a message to all its streams if the level of the message is equal to or higher than its own level.

### `FileLoggingStream`

This is a class defined in the `streams.py` file. It implements the `Writable` interface and represents a file as a writable stream. It has a `write` method that writes a string to the file and a `flush` method that flushes the file.
