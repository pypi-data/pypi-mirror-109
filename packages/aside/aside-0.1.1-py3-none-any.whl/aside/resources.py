"""Manages the package resource files."""

import locale

try:
    from importlib.abc import Traversable
except ImportError:
    from importlib_resources.abc import Traversable

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

from .boilerplate import language
from .config import config
from .theme import theme

__all__ = [
    "get_resource",
    "get_svg",
]


root: Traversable = files(__package__) / "_resources"
"""The root traversable resource location.

See :any:`importlib_resources<importlib_resources:using>`
and :py:mod:`importlib.resources` for more information.

:meta hide-value:
"""


def str_replace_swap(string: str, this: str, that: str) -> str:
    """Replace all ``this`` and ``that`` tokens in the ``string``, swapping them."""
    # Sanity checks
    assert "%placeholder%" not in string
    assert this != that
    assert this not in that

    string = string.replace(this, "%placeholder%")
    string = string.replace(that, this)
    string = string.replace("%placeholder%", that)

    return string


def find_resource(
    name: str,
    interpolated: bool,
    localized: bool,
) -> Traversable:
    """Find the resource location given the resource name.

    See `get_resource` for more info.
    """
    res = [name]

    # This insane piece of code is required because
    # LC_MESSAGES may not exist on some windows python installs
    message_cat = getattr(locale, "LC_MESSAGES", locale.LC_CTYPE)

    lang = language.get_lang(message_cat)
    if localized and lang:
        res.extend([lang + "/" + n for n in res])

    if interpolated:
        res.extend([n + ".int" for n in res])

    res = [root / n for n in res]
    res = [p for p in res if p.exists()]
    if not res:
        raise RuntimeError(f"Missing resource '{name}'")

    return res[-1]


def load_resource(
    path: Traversable,
    do_interpolate: bool,
) -> str:
    """Load the resource contents given the traversable resource path.

    See `get_resource` for more info.
    """
    contents = path.read_text(encoding="utf-8")

    if do_interpolate:
        contents = str_replace_swap(contents, "{{", "{")
        contents = str_replace_swap(contents, "}}", "}")
        contents = contents.format(config=config, theme=theme)

    return contents


def get_resource(
    name: str,
    interpolated: bool = True,
    localized: bool = True,
) -> str:
    """Find and load the resource given its name.

    This function also takes into account interpolatable and localized resource
    overrides.

    - **Interpolatable** resources are resource files which have an extra ``.int``
      file extension. After loading an interpolatable resource, all strings of
      the form ``{{config.something}}`` and ``{{theme.other}}`` are interpolated
      with the values from the current `aside.config.config` and
      `aside.theme.theme`.

    - **Localized** resources are resources from the ``LOCALE``-specific resource
      directory. The locale is determined by ``LC_MESSAGES``. For example, the
      ``ru/icon.svg`` resource is the localized version of the ``icon.svg``
      resource, corresponding to ``LC_MESSAGES="ru_RU.UTF-8"``.

    Args:
        name: The name of the resource to load.
        interpolated: Whether to search for interpolatable resources.
        localized: Whether to search for localized resources.

    Returns:
        The loaded resource contents.
    """
    res = find_resource(name, interpolated=interpolated, localized=localized)
    res = load_resource(res, do_interpolate=res.suffix == ".int")
    return res


def get_svg(name: str) -> bytes:
    """Find and load an svg resource specified by ``name``.

    Args:
        name: The name of the svg resource without the file extension.

    Returns:
        The contents of the resource, suitable to be loaded with
        :py:meth:`PyQt5.QtGui.QPixmap.loadFromData`.
    """
    return get_resource(name + ".svg").encode()
