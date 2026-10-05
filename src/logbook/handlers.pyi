from __future__ import annotations

import os
import ssl
from collections import deque
from collections.abc import Callable, Mapping
from datetime import datetime, timedelta
from types import TracebackType
from typing import IO, TYPE_CHECKING, BinaryIO, Literal, Self

if TYPE_CHECKING:
    from threading import RLock

    from logbook.base import LogLevel, LogRecord

from _typeshed import Incomplete

from logbook.base import LogRecord

class Handler:
    blackhole: bool
    level: LogLevel
    formatter: Formatter | None
    filter: LogFilter | None
    bubble: bool
    stack_manager: Incomplete

    def __init__(
        self,
        level: int | str = ...,
        filter: LogFilter | None = ...,
        bubble: bool = False,
    ) -> None: ...
    @property
    def level_name(self) -> str: ...
    def format(self, record: LogRecord) -> str: ...
    def should_handle(self, record: LogRecord) -> bool: ...
    def handle(self, record: LogRecord) -> bool: ...
    def emit(self, record: LogRecord) -> None: ...
    def emit_batch(self, records: list[LogRecord], reason: str) -> None: ...
    def close(self) -> None: ...
    def handle_error(
        self,
        record: LogRecord,
        exc_info: tuple[type[BaseException], BaseException, TracebackType],
    ) -> None: ...
    def push_application(self) -> None: ...
    def pop_application(self) -> None: ...
    def push_context(self) -> None: ...
    def pop_context(self) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...

class Formatter:
    def __call__(self, record: LogRecord, handler: Handler) -> str: ...

class StringFormatter(Formatter):
    format_string: str

    def __init__(self, format_string: str) -> None: ...
    def format_record(self, record: LogRecord, handler: Handler) -> str: ...
    def format_exception(self, record: LogRecord) -> str | None: ...

class StringFormatterHandlerMixin:
    default_format_string: str
    formatter_class: type[StringFormatter]
    format_string: str | None

    def __init__(self, format_string: str | None) -> None: ...

class HashingHandlerMixin:
    def hash_record_raw(self, record: LogRecord) -> Incomplete: ...
    def hash_record(self, record: LogRecord) -> str: ...

class LimitingHandlerMixin(HashingHandlerMixin):
    record_limit: int | None
    record_delta: timedelta

    def __init__(
        self,
        record_limit: int | None,
        record_delta: timedelta | int | float | None,
    ) -> None: ...
    def check_delivery(self, record: LogRecord) -> tuple[int, bool]: ...

class StreamHandler(Handler, StringFormatterHandlerMixin):
    stream: IO[str] | None
    lock: RLock
    encoding: str | None

    def __init__(
        self,
        stream: Incomplete = ...,
        level: int | str = ...,
        format_string: str | None = ...,
        encoding: str | None = ...,
        filter: LogFilter | None = ...,
        bubble: bool = False,
    ) -> None: ...
    def ensure_stream_is_open(self) -> None: ...
    def close(self) -> None: ...
    def flush(self) -> None: ...
    def encode(self, msg: str) -> str: ...
    def write(self, item: str) -> None: ...
    def should_flush(self) -> bool: ...

class FileHandler(StreamHandler):
    def __init__(
        self,
        filename: str | bytes | os.PathLike[str],
        mode: str = 'a',
        encoding: str | None = ...,
        level: int | str = ...,
        format_string: str | None = ...,
        delay: bool = False,
        filter: LogFilter | None = ...,
        bubble: bool = False,
    ) -> None: ...
    def _open(self, mode: str | None = None) -> None: ...

class GZIPCompressionHandler(FileHandler):
    def __init__(
        self,
        filename: str | bytes | os.PathLike[str],
        encoding: str | None = ...,
        level: int | str = ...,
        format_string: str | None = ...,
        delay: bool = False,
        filter: LogFilter | None = ...,
        bubble: bool = False,
        compression_quality: int = 9,
    ) -> None: ...

class BrotliCompressionHandler(FileHandler):
    def __init__(
        self,
        filename: str | bytes | os.PathLike[str],
        encoding: str | None = ...,
        level: int | str = ...,
        format_string: str | None = ...,
        delay: bool = False,
        filter: LogFilter | None = ...,
        bubble: bool = False,
        compression_window_size: int = ...,
        compression_quality: int = 11,
    ) -> None: ...

class MonitoringFileHandler(FileHandler):
    def __init__(
        self,
        filename: str | bytes | os.PathLike[str],
        mode: str = 'a',
        encoding: str = 'utf-8',
        level: int | str = ...,
        format_string: str | None = ...,
        delay: bool = False,
        filter: LogFilter | None = ...,
        bubble: bool = False,
    ) -> None: ...
    def emit(self, record: LogRecord) -> None: ...

class StderrHandler(StreamHandler):
    stream: IO[str]

    def __init__(
        self,
        level: int | str = ...,
        format_string: str | None = ...,
        filter: LogFilter | None = ...,
        bubble: bool = False,
    ) -> None: ...

class RotatingFileHandler(FileHandler):
    max_size: int
    backup_count: int

    def __init__(
        self,
        filename: str | bytes | os.PathLike[str],
        mode: str = 'a',
        encoding: str = 'utf-8',
        level: int | str = ...,
        format_string: str | None = ...,
        delay: bool = False,
        max_size: int = ...,
        backup_count: int = 5,
        filter: LogFilter | None = ...,
        bubble: bool = False,
    ) -> None: ...
    def should_rollover(self, record: LogRecord, bytes: int) -> bool: ...
    def perform_rollover(self) -> None: ...
    def emit(self, record: LogRecord) -> None: ...

class TimedRotatingFileHandler(FileHandler):
    date_format: str
    backup_count: int
    rollover_format: str
    original_filename: str
    basename: str
    ext: str
    timed_filename_for_current: bool
    _timestamp: str

    def __init__(
        self,
        filename: str | bytes | os.PathLike[str],
        mode: str = 'a',
        encoding: str = 'utf-8',
        level: int | str = ...,
        format_string: str | None = ...,
        date_format: str = '%Y-%m-%d',
        backup_count: int = 0,
        filter: LogFilter | None = ...,
        bubble: bool = False,
        timed_filename_for_current: bool = True,
        rollover_format: str = '{basename}-{timestamp}{ext}',
    ) -> None: ...
    def _get_timestamp(self, datetime: datetime) -> str: ...
    def generate_timed_filename(self, timestamp: str) -> str: ...
    def files_to_delete(self) -> list[tuple[float, str]]: ...
    def perform_rollover(self, new_timestamp: str) -> None: ...
    def emit(self, record: LogRecord) -> None: ...

class TestHandler(Handler, StringFormatterHandlerMixin):
    default_format_string: str
    records: list[LogRecord]
    formatted_records: list[str]
    has_criticals: bool
    has_errors: bool
    has_warnings: bool
    has_notices: bool
    has_infos: bool
    has_debugs: bool
    has_traces: bool

    def __init__(
        self,
        level: int | str = ...,
        format_string: str | None = ...,
        filter: LogFilter | None = ...,
        bubble: bool = False,
        force_heavy_init: bool = False,
    ) -> None: ...
    def close(self) -> None: ...
    def emit(self, record: LogRecord) -> None: ...
    def has_critical(self, *args: Incomplete, **kwargs: Incomplete) -> bool: ...
    def has_error(self, *args: Incomplete, **kwargs: Incomplete) -> bool: ...
    def has_warning(self, *args: Incomplete, **kwargs: Incomplete) -> bool: ...
    def has_notice(self, *args: Incomplete, **kwargs: Incomplete) -> bool: ...
    def has_info(self, *args: Incomplete, **kwargs: Incomplete) -> bool: ...
    def has_debug(self, *args: Incomplete, **kwargs: Incomplete) -> bool: ...
    def has_trace(self, *args: Incomplete, **kwargs: Incomplete) -> bool: ...

class MailHandler(Handler, StringFormatterHandlerMixin, LimitingHandlerMixin):
    default_format_string: str
    default_related_format_string: str
    default_subject: str
    max_record_cache: int
    record_cache_prune: float
    from_addr: str
    recipients: list[str] | str
    subject: str
    server_addr: tuple[str, int] | str | None
    credentials: tuple[str, ...] | Mapping[str, Incomplete] | None
    secure: bool | ssl.SSLContext | None
    related_format_string: str | None
    starttls: bool
    timeout: float | None

    def __init__(
        self,
        from_addr: str,
        recipients: list[str] | str,
        subject: str | None = ...,
        server_addr: tuple[str, int] | str | None = ...,
        credentials: tuple[str, ...] | Mapping[str, Incomplete] | None = ...,
        secure: bool
        | ssl.SSLContext
        | tuple[str, str]
        | Mapping[str, str]
        | None = ...,
        record_limit: int | None = ...,
        record_delta: timedelta | int | float | None = ...,
        level: int | str = ...,
        format_string: str | None = ...,
        related_format_string: str | None = ...,
        filter: LogFilter | None = ...,
        bubble: bool = False,
        starttls: bool = True,
        timeout: float | None = 5.0,
    ) -> None: ...
    def get_recipients(self, record: LogRecord) -> list[str] | str: ...
    def message_from_record(self, record: LogRecord, suppressed: int) -> Incomplete: ...
    def format_related_record(self, record: LogRecord) -> str | None: ...
    def generate_mail(self, record: LogRecord, suppressed: int = 0) -> Incomplete: ...
    def collapse_mails(
        self, mail: Incomplete, related: list[str], reason: str
    ) -> Incomplete: ...
    def get_connection(self) -> Incomplete: ...
    def close_connection(self, con: Incomplete | None) -> None: ...
    def deliver(self, msg: Incomplete, recipients: list[str] | str) -> None: ...
    def emit(self, record: LogRecord) -> None: ...
    def emit_batch(self, records: list[LogRecord], reason: str) -> None: ...

class GMailHandler(MailHandler):
    def __init__(
        self,
        account_id: str,
        password: str,
        recipients: list[str] | str,
        **kwargs: Incomplete,
    ) -> None: ...

class SyslogHandler(Handler, StringFormatterHandlerMixin):
    default_format_string: str
    LOG_EMERG: Literal[0]
    LOG_ALERT: Literal[1]
    LOG_CRIT: Literal[2]
    LOG_ERR: Literal[3]
    LOG_WARNING: Literal[4]
    LOG_NOTICE: Literal[5]
    LOG_INFO: Literal[6]
    LOG_DEBUG: Literal[7]
    LOG_KERN: Literal[0]
    LOG_USER: Literal[1]
    LOG_MAIL: Literal[2]
    LOG_DAEMON: Literal[3]
    LOG_AUTH: Literal[4]
    LOG_SYSLOG: Literal[5]
    LOG_LPR: Literal[6]
    LOG_NEWS: Literal[7]
    LOG_UUCP: Literal[8]
    LOG_CRON: Literal[9]
    LOG_AUTHPRIV: Literal[10]
    LOG_FTP: Literal[11]
    LOG_LOCAL0: Literal[16]
    LOG_LOCAL1: Literal[17]
    LOG_LOCAL2: Literal[18]
    LOG_LOCAL3: Literal[19]
    LOG_LOCAL4: Literal[20]
    LOG_LOCAL5: Literal[21]
    LOG_LOCAL6: Literal[22]
    LOG_LOCAL7: Literal[23]
    facility_names: dict[str, int]
    level_priority_map: dict[int, int]
    application_name: str | None
    address: str | tuple[str, int]
    remote_address: str | tuple[str, int]
    facility: str
    socktype: int
    unixsocket: bool
    socket: Incomplete
    enveloper: Callable[[LogRecord], Incomplete]
    record_delimiter: str
    connection_exception: type[OSError]

    def __init__(
        self,
        application_name: str | None = ...,
        address: str | tuple[str, int] | None = ...,
        facility: str = 'user',
        socktype: int = ...,
        level: int | str = ...,
        format_string: str | None = ...,
        filter: LogFilter | None = ...,
        bubble: bool = False,
        record_delimiter: str | None = ...,
    ) -> None: ...
    def encode_priority(self, record: LogRecord) -> int: ...
    def wrap_segments(self, record: LogRecord, before: str) -> Incomplete: ...
    def unix_envelope(self, record: LogRecord) -> Incomplete: ...
    def net_envelope(self, record: LogRecord) -> Incomplete: ...
    def emit(self, record: LogRecord) -> None: ...
    def send_to_socket(self, data: bytes) -> None: ...
    def close(self) -> None: ...

class NTEventLogHandler(Handler, StringFormatterHandlerMixin):
    dllname: str | None
    default_format_string: str
    application_name: str
    log_type: str

    def __init__(
        self,
        application_name: str,
        log_type: str = 'Application',
        level: int | str = ...,
        format_string: str | None = ...,
        filter: LogFilter | None = ...,
        bubble: bool = False,
    ) -> None: ...
    def unregister_logger(self) -> None: ...
    def get_event_type(self, record: LogRecord) -> int: ...
    def get_event_category(self, record: LogRecord) -> int: ...
    def get_message_id(self, record: LogRecord) -> int: ...

class WrapperHandler(Handler):
    _direct_attrs: frozenset[str]
    handler: Handler

    def __init__(self, handler: Handler) -> None: ...

class FingersCrossedHandler(Handler):
    batch_emit_reason: str
    lock: RLock
    buffered_records: deque[LogRecord]
    buffer_size: int
    triggered: bool

    def __init__(
        self,
        handler: Handler | Callable[[LogRecord, FingersCrossedHandler], Handler],
        action_level: int | str = ...,
        buffer_size: int = 0,
        pull_information: bool = True,
        reset: bool = False,
        filter: LogFilter | None = ...,
        bubble: bool = False,
    ) -> None: ...
    def close(self) -> None: ...
    def enqueue(self, record: LogRecord) -> bool: ...
    def rollover(self, record: LogRecord) -> None: ...
    def emit(self, record: LogRecord) -> None: ...

class GroupHandler(WrapperHandler):
    pull_information: bool
    buffered_records: list[LogRecord]

    def __init__(
        self,
        handler: Handler,
        pull_information: bool = True,
    ) -> None: ...
    def rollover(self) -> None: ...
    def pop_application(self) -> None: ...
    def pop_context(self) -> None: ...
    def emit(self, record: LogRecord) -> None: ...

class NullHandler(Handler):
    def __init__(
        self,
        level: int | str = ...,
        filter: LogFilter | None = ...,
    ) -> None: ...

type LogFilter = Callable[[LogRecord, Handler], bool]

def create_syshandler(
    application_name: str, level: int | str = ...
) -> SyslogHandler | NTEventLogHandler: ...

__all__ = [
    'Handler',
    'Formatter',
    'StringFormatter',
    'StringFormatterHandlerMixin',
    'HashingHandlerMixin',
    'LimitingHandlerMixin',
    'StreamHandler',
    'FileHandler',
    'GZIPCompressionHandler',
    'BrotliCompressionHandler',
    'MonitoringFileHandler',
    'StderrHandler',
    'RotatingFileHandler',
    'TimedRotatingFileHandler',
    'TestHandler',
    'MailHandler',
    'GMailHandler',
    'SyslogHandler',
    'NTEventLogHandler',
    'WrapperHandler',
    'FingersCrossedHandler',
    'GroupHandler',
    'NullHandler',
    'LogFilter',
    'create_syshandler',
]
