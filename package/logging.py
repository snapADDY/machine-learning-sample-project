import logging
import sys

DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40

LEVELS = {"DEBUG": DEBUG, "INFO": INFO, "WARNING": WARNING, "ERROR": ERROR}

DEFAULT_FORMAT = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
DEBUG_FORMAT = logging.Formatter("[%(asctime)s] %(name)s:%(lineno)d [%(levelname)s] %(message)s")


class Logger:
    """Basic logger."""

    def __init__(self, name: str):
        """Initialize logger.

        Parameters
        ----------
        name : str
            Name of the logger. This is intended to be `__name__`.
        """
        self.name = name

        # return a logger with the specified name, creating it if necessary
        self._logger = logging.getLogger(name)

        # stream handler to stdout
        self._stream_handler = logging.StreamHandler(sys.stdout)
        self._logger.addHandler(self._stream_handler)

        # set level of both the logger and the handler
        self.set_level("INFO")

    def set_level(self, level: str | int):
        """Set the logger's level.

        Parameters
        ----------
        level : str | int
            Level to set the logger to.
        """
        # translate string to integer
        if isinstance(level, str):
            level = LEVELS[level.upper()]

        # set the logger's level
        self._logger.setLevel(level)

        # and all handlers
        for handler in self._logger.handlers:
            handler.setLevel(level)

            # optionally change the formatter (log more when in debug mode)
            if level < INFO:
                handler.setFormatter(DEBUG_FORMAT)
            else:
                handler.setFormatter(DEFAULT_FORMAT)

    def debug(self, message: str) -> None:
        """Debug log message.

        Parameters
        ----------
        message : str
            Message to log.
        """
        if self._logger.isEnabledFor(DEBUG):
            self._logger._log(DEBUG, message, ())

    def info(self, message: str) -> None:
        """Info log message.

        Parameters
        ----------
        message : str
            Message to log.
        """
        if self._logger.isEnabledFor(INFO):
            self._logger._log(INFO, message, ())

    def warning(self, message: str) -> None:
        """Warning log message.

        Parameters
        ----------
        message : str
            Message to log.
        """
        if self._logger.isEnabledFor(WARNING):
            self._logger._log(WARNING, message, ())

    def error(self, message: str | Exception) -> None:
        """Error log message.

        Parameters
        ----------
        message : str
            Message to log.
        """
        if self._logger.isEnabledFor(ERROR):
            if isinstance(message, Exception):
                # log stacktrace if message is an exception
                self._logger._log(ERROR, message, (), exc_info=True)
            else:
                self._logger._log(ERROR, message, ())

    @property
    def in_debug_mode(self) -> bool:
        """Check if the logger's level is DEBUG.

        Returns
        -------
        bool
            True, if logger is in DEBUG mode, False otherwise.
        """
        return self._logger.level == DEBUG

    @property
    def level(self) -> int:
        """Return the current log level.

        Returns
        -------
        int
            Log level.
        """
        return self._logger.level

    def __repr__(self) -> str:
        """Representation of the logger."""
        return f"<Logger: {self.name} ({self.level})>"
