from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from logbook.base import LogRecord
    from logbook.handlers import Handler, LogFilter

from _typeshed import Incomplete

from logbook.base import NOTSET, RecordDispatcher, dispatch_record
from logbook.handlers import (
    Handler,
    StderrHandler,
    StringFormatterHandlerMixin,
)

class BackendBase:
    options: dict[str, Incomplete]
    def __init__(self, **options: Incomplete) -> None: ...
    def setup_backend(self) -> None: ...
    def record_ticket(
        self, record: LogRecord, data: Incomplete, hash: str, app_id: str
    ) -> None: ...
    def count_tickets(self) -> int: ...
    def get_tickets(
        self, order_by: str = '-last_occurrence_time', limit: int = 50, offset: int = 0
    ) -> list[Incomplete]: ...
    def solve_ticket(self, ticket_id: Incomplete) -> None: ...
    def delete_ticket(self, ticket_id: Incomplete) -> None: ...
    def get_ticket(self, ticket_id: Incomplete) -> Incomplete | None: ...
    def get_occurrences(
        self,
        ticket: Incomplete,
        order_by: str = '-time',
        limit: int = 50,
        offset: int = 0,
    ) -> list[Incomplete]: ...

class CouchDBBackend(BackendBase):
    database: Incomplete

    def setup_backend(self) -> None: ...
    def record_ticket(
        self, record: LogRecord, data: Incomplete, hash: str, app_id: str
    ) -> None: ...

class TaggingLogger(RecordDispatcher):
    def __init__(
        self, name: str | None = None, tags: list[str] | None = None
    ) -> None: ...
    def log(
        self,
        tags: str | list[str],
        msg: str,
        *args: Incomplete,
        exc_info: Incomplete = None,
        extra: dict[str, Incomplete] | None = None,
        frame_correction: int = 0,
        **kwargs: Incomplete,
    ) -> None: ...

class TaggingHandler(Handler):
    _handlers: dict[str, list[Handler]]

    def __init__(
        self,
        handlers: dict[str, Handler | list[Handler]],
        filter: LogFilter | None = None,
        bubble: bool = False,
    ) -> None: ...
    def emit(self, record: LogRecord) -> None: ...

class SlackHandler(Handler, StringFormatterHandlerMixin):
    channel: str
    slack: Incomplete

    def __init__(
        self,
        api_token: str,
        channel: str,
        level: int | str = NOTSET,
        format_string: str | None = None,
        filter: LogFilter | None = None,
        bubble: bool = False,
    ) -> None: ...
    def emit(self, record: LogRecord) -> None: ...

class JinjaFormatter:
    template: Incomplete

    def __init__(self, template: str) -> None: ...
    def __call__(self, record: LogRecord, handler: Handler) -> str: ...

class ExternalApplicationHandler(Handler):
    encoding: str

    def __init__(
        self,
        arguments: list[str],
        stdin_format: str | None = None,
        encoding: str = 'utf-8',
        level: int | str = NOTSET,
        filter: LogFilter | None = None,
        bubble: bool = False,
    ) -> None: ...
    def emit(self, record: LogRecord) -> None: ...

class ColorizingStreamHandlerMixin:
    _use_color: bool | None

    def force_color(self) -> None: ...
    def forbid_color(self) -> None: ...
    def should_colorize(self, record: LogRecord) -> bool: ...
    def get_color(self, record: LogRecord) -> str: ...
    def format(self, record: LogRecord) -> str: ...

class ColorizedStderrHandler(ColorizingStreamHandlerMixin, StderrHandler):
    def __init__(self, *args: Incomplete, **kwargs: Incomplete) -> None: ...

class ExceptionHandler(Handler, StringFormatterHandlerMixin):
    exc_type: type[BaseException]

    def __init__(
        self,
        exc_type: type[BaseException],
        level: int | str = NOTSET,
        format_string: str | None = None,
        filter: LogFilter | None = None,
        bubble: bool = False,
    ) -> None: ...
    def handle(self, record: LogRecord) -> bool: ...

class DedupHandler(Handler):
    def __init__(
        self,
        format_string: str = 'message repeated {count} times: {message}',
        *args: Incomplete,
        **kwargs: Incomplete,
    ) -> None: ...
    def clear(self) -> None: ...
    def pop_application(self) -> None: ...
    def pop_thread(self) -> None: ...
    def pop_context(self) -> None: ...
    def pop_greenlet(self) -> None: ...
    def handle(self, record: LogRecord) -> bool: ...
    def flush(self) -> None: ...

class RiemannHandler(Handler):
    host: str
    port: int
    ttl: int
    queue: list[dict[str, Incomplete]]
    flush_threshold: int
    transport: type[Incomplete]

    def __init__(
        self,
        host: str,
        port: int,
        message_type: Literal['tcp', 'udp', 'test'] = 'tcp',
        ttl: int = 60,
        flush_threshold: int = 10,
        bubble: bool = False,
        filter: LogFilter | None = None,
        level: int | str = NOTSET,
    ) -> None: ...
    def record_to_event(self, record: LogRecord) -> dict[str, Incomplete]: ...
    def _flush_events(self) -> None: ...
    def emit(self, record: LogRecord) -> None: ...

__all__ = [
    'CouchDBBackend',
    'TaggingLogger',
    'TaggingHandler',
    'SlackHandler',
    'JinjaFormatter',
    'ExternalApplicationHandler',
    'ColorizingStreamHandlerMixin',
    'ColorizedStderrHandler',
    'ExceptionHandler',
    'DedupHandler',
    'RiemannHandler',
]
