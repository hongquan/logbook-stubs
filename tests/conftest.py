from __future__ import annotations

from typing import TYPE_CHECKING

import logbook
import pytest


if TYPE_CHECKING:
    from logbook.base import Logger


@pytest.fixture
def logger() -> Logger:
    return logbook.Logger('testlogger')
