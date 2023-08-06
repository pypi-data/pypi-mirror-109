"""Implements human-readable datetime tools."""

import locale
from datetime import datetime
from typing import Dict, Optional

from arrow import Arrow
from dateparser import parse

from . import language

__all__ = [
    "relative_to_absolute",
    "absolute_to_relative",
]


dateparser_settings: Dict = dict(
    RETURN_AS_TIMEZONE_AWARE=True,
    DATE_ORDER="DMY",
    PREFER_DAY_OF_MONTH="first",
    PREFER_DATES_FROM="future",
    PARSERS=["relative-time", "absolute-time"],
)


def relative_to_absolute(relative: str) -> Optional[datetime]:
    """Try to convert a relative time string like ``in 1 hour`` to a ``datetime``."""
    return parse(
        relative,
        languages=("en", language.get_lang(locale.LC_TIME)),
        settings=dateparser_settings,
    )


def absolute_to_relative(absolute: datetime) -> str:
    """Convert a ``datetime`` to a relative time string in the current language."""
    return Arrow.fromdatetime(absolute).humanize(
        locale=language.get_lang(locale.LC_TIME)
    )
