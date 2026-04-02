"""
Rich logging manager.
"""
# MARK: Imports
import logging
import logging.handlers
from pathlib import Path
from typing import Optional

from rich.logging import RichHandler

# MARK: Classes
class LoggerManager:
    """
    Manages logging configuration and logger instances.
    """
    # MARK: Constants
    LOG_LEVELS: dict[str, int] = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    # MARK: Initializer
    def __init__(self,
        logFile: Path,
        logLevel: int = logging.INFO,
        consoleOutput: bool = True,
        logFormat: str = f"[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
        dateFormat: str = "%Y-%m-%d %H:%M:%S",
        maxLogFileSize: int = 10 * 1024 * 1024, # 10MB
        backupCount: int = 5
    ) -> None:
        """
        logFile: The path to the log file.
        logLevel: The default log level.
        consoleOutput: Whether to output logs to the console.
        logFormat: The format of the log messages.
        dateFormat: The format of the date in the log messages.
        maxLogFileSize: The maximum size of the log file before it is rotated.
        backupCount: The number of backup log files to keep.
        """
        # Properties
        self.isDebug = (logLevel == logging.DEBUG)
        self._logLevel = logLevel
        self._loggers: dict[str, logging.Logger] = {}

        # Prepare log file path
        self.logPath = Path(logFile).resolve()
        self.logPath.parent.mkdir(parents=True, exist_ok=True)

        # Configure root logger
        rootLogger = logging.getLogger()
        rootLogger.setLevel(logging.WARNING)
        rootLogger.handlers.clear()

        # Create formatter
        formatter = logging.Formatter(
            fmt=logFormat,
            datefmt=dateFormat
        )

        # File handler with rotation
        fileHandler = logging.handlers.RotatingFileHandler(
            filename=str(self.logPath),
            maxBytes=maxLogFileSize,
            backupCount=backupCount,
            encoding="utf-8"
        )
        fileHandler.setLevel(logLevel)
        fileHandler.setFormatter(formatter)
        self._handlers: list[logging.Handler] = [fileHandler]

        # Console handler (optional)
        if consoleOutput:
            consoleHandler = RichHandler(
                show_level=False,
                show_time=False,
                show_path=False
            )
            consoleHandler.setLevel(logLevel)
            consoleHandler.setFormatter(formatter)
            self._handlers.append(consoleHandler)

    # MARK: Functions
    def getLogger(self, name: str, logLevel: Optional[int] = None) -> logging.Logger:
        """
        Get or create a logger with the specified name.
        Loggers are cached, so calling this multiple times with the same name returns the same logger instance.

        name: The name of the logger.
        logLevel: The log level for the logger. Defaults to the default log level if `None`.

        Returns a `logging.Logger` instance.
        """
        # Return cached logger if exists
        if name in self._loggers:
            logger = self._loggers[name]
            if logLevel is not None:
                logger.setLevel(logLevel)
            return logger

        # Create new logger
        logger = logging.getLogger(name)
        logger.propagate = False

        for handler in self._handlers:
            logger.addHandler(handler)

        # Set log level if specified
        logger.setLevel(logLevel if logLevel is not None else self._logLevel)

        # Cache the logger
        self._loggers[name] = logger

        return logger

    def setLogLevel(self, level: int) -> None:
        """
        Set the global log level for all loggers.

        level: Logging level (e.g., `logging.DEBUG`, `logging.INFO`, etc.)
        """
        self._logLevel = level

        for handler in self._handlers:
            handler.setLevel(level)

        for logger in self._loggers.values():
            logger.setLevel(level)

        self.isDebug = (level == logging.DEBUG)

    def disableTerminalLogs(self) -> None:
        """
        Disable logging to the terminal.
        """
        rootLogger = logging.getLogger()
        rootLogger.handlers = [
            handler for handler in rootLogger.handlers
            if not isinstance(handler, RichHandler)
        ]

    def disableByName(self, name: str) -> None:
        """
        Disable all handlers (console and file) for a specific logger by name, if it exists.
        No error is raised if the logger does not exist.

        name: The name of the logger to disable handlers for.
        """
        if (logger := self.getLogger(name)) is not None:
            logger.handlers.clear()
            logger.propagate = False
