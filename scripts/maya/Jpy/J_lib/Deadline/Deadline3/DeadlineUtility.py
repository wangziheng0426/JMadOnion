from __future__ import absolute_import
import sys

try:
    from typing import Any, Iterable, Text, Union
except ImportError:
    # Not available in stdlib for python 2
    pass


def ArrayToCommaSeparatedString(iterable):
    # type: (Any) -> Union[str, Text]
    """Helper function to separate arrays into strings."""
    if is_string_type(iterable):
        return iterable

    if iterable is None:
        return ""

    return ",".join(str(x) for x in iterable)


def is_string_type(value):
    # type: (Any) -> bool
    """Function to determine if value is a string type.
    This function exists to allow type-hinting to function properly
    """
    string_type = str
    if sys.version_info.major == 2:
        string_type = basestring  # type: ignore # basestring doesn't exist in py3

    if isinstance(value, string_type):
        return True

    return False
