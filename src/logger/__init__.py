from typing import Callable, Any

from .colors import Color

class Logger:

    def __init__(self, display_logs: bool = True, display_layer: int = 0) -> None:
        self.logs = []
        self.display_logs = display_logs
        self.display_layer = display_layer

    # For messages, which will pop up very often
    # For messages, which show some commands output
    def spam(self, message: str, from_: Callable[[Any, ...], Any]) -> None:
        self._log_any(message, from_, "SPAM", Color.SPAM, Color.SPAM_ID)

    # For messages, which tells at what stage checker/debugger currently is
    # For messages, after receiving some requests
    def debug(self, message: str, from_: Callable[[Any, ...], Any]) -> None:
        self._log_any(message, from_, "DEBUG", Color.DEBUG, Color.DEBUG_ID)

    # For user submissions related little errors
    def warn(self, message: str, from_: Callable[[Any, ...], Any]) -> None:
        self._log_any(message, from_, "WARNING", Color.WARNING, Color.WARNING_ID)

    # For server operation related little errors
    def alert(self, message: str, from_: Callable[[Any, ...], Any]) -> None:
        self._log_any(message, from_, "ALERT", Color.ALERT, Color.ALERT_ID)

    # For important server errors
    def error(self, message: str, from_: Callable[[Any, ...], Any]) -> None:
        self._log_any(message, from_, "ERROR", Color.ERROR, Color.ERROR_ID)

    # For general information about server procedures
    def info(self, message: str, from_: Callable[[Any, ...], Any]) -> None:
        self._log_any(message, from_, "INFO", Color.INFO, Color.INFO_ID)

    def _log_any(self, message: str, from_: Callable[[Any, ...], Any], type_: str, color: str, id_: int) -> None:
        if "__self__" in from_.__dir__():
            self.logs.append(f"{Color.FROM}FROM: {from_.__self__.__class__.__name__}.{from_.__name__} {color}{type_}:{Color.NORMAL} {message}")
        else:
            self.logs.append(f"{Color.FROM}FROM: {from_.__name__ if from_.__name__ != 'main' else 'app.main'} {color}{type_}:{Color.NORMAL} {message}")

        if self.display_logs and self.display_layer <= id_:
            print(self.logs[-1])
