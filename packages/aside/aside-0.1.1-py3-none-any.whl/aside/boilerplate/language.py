"""Common code for language and locale settings."""

import locale
from typing import Optional

__all__ = [
    "get_lang",
]


def get_locale(category: int) -> Optional[str]:
    """Get the current locale for the category (can be overriden by config)."""
    # load current config on-demand to avoid circular import
    from ..config import config  # pylint: disable=import-outside-toplevel

    if config.locale is not None:
        return config.locale

    loc, _ = locale.getlocale(category)
    return loc


def get_lang(category: int) -> Optional[str]:
    """Get the current language for the category (can be overriden by config)."""
    loc = get_locale(category)
    if not loc:
        return None

    lang, _ = loc.split("_")
    return lang
