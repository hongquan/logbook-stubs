from __future__ import annotations

import logging
import sys
import warnings
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from types import FrameType, TracebackType
from typing import Any

from _typeshed import Incomplete

import logbook
from logbook.base import LogLevel, LogRecord
from logbook.handlers import Handler

_ExcInfo = (
    tuple[type[BaseException], BaseException, TracebackType] | tuple[None, None, None]
)

_ShowWarningFunc = Callable[
    [str, type[Warning], str, int, Any | None, str | None], None
]
_FilterType = tuple[Any, ...]

def redirect_logging(set_root_logger_level: bool = True) -> None: ...

class redirected_logging:
    old_handlers: list[logging.Handler]
    old_level: int
    set_root_logger_level: bool

    def __init__(self, set_root_logger_level: bool = True) -> None: ...
    def start(self) -> None: ...
    def end(
        self,
        etype: type[BaseException] | None = None,
        evalue: BaseException | None = None,
        tb: TracebackType | None = None,
    ) -> None: ...
    __enter__ = start
    __exit__ = end

class LoggingCompatRecord(logbook.LogRecord):
    def _format_message(
        self, msg: str, *args: Incomplete, **kwargs: Incomplete
    ) -> str: ...

class RedirectLoggingHandler(logging.Handler):
    def __init__(self) -> None: ...
    def convert_level(self, level: int) -> LogLevel: ...
    def find_extra(self, old_record: logging.LogRecord) -> dict[str, Incomplete]: ...
    def find_caller(self, old_record: logging.LogRecord) -> FrameType | None: ...
    def convert_time(self, timestamp: float) -> datetime: ...
    def convert_record(self, old_record: logging.LogRecord) -> LoggingCompatRecord: ...
    def emit(self, record: logging.LogRecord) -> None: ...

class LoggingHandler(logbook.Handler):
    logger: logging.Logger

    def __init__(
        self,
        logger: logging.Logger | str | None = None,
        level: int | str = logbook.NOTSET,
        filter: Incomplete = None,
        bubble: bool = False,
    ) -> None: ...
    def get_logger(self, record: LogRecord) -> logging.Logger: ...
    def convert_level(self, level: int) -> int: ...
    def convert_time(self, dt: datetime) -> float: ...
    def convert_record(self, old_record: LogRecord) -> logging.LogRecord: ...
    def emit(self, record: LogRecord) -> None: ...

def redirect_warnings() -> None: ...

class redirected_warnings:
    _entered: bool
    _filters: list[_FilterType]
    _showwarning: _ShowWarningFunc

    def __init__(self) -> None: ...
    def message_to_unicode(self, message: object) -> str: ...
    def make_record(
        self, message: str, exception: type[Warning], filename: str, lineno: int
    ) -> LogRecord: ...
    def start(self) -> None: ...
    def end(
        self,
        etype: type[BaseException] | None = None,
        evalue: BaseException | None = None,
        tb: TracebackType | None = None,
    ) -> None: ...
    __enter__ = start
    __exit__ = end

__all__ = [
    'redirect_logging',
    'redirected_logging',
    'LoggingCompatRecord',
    'RedirectLoggingHandler',
    'LoggingHandler',
    'redirect_warnings',
    'redirected_warnings',
]
