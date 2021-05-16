"""Retention methods."""
import math
from config import settings
from typing import Union


def calculate_retention(file_size: int, min_age: Union[int, None] = None,
                        max_age: Union[int, None] = None,
                        max_size: Union[int, None] = None) -> int:
    """Calculate the file retention for a specified file size.

    Args:
        file_size (int): The size of the file in Mb.
        min_age (Union[int, None]): The minimum age of the file. Defaults to
            the configuration file's value.
        max_age (Union[int, None]): The maximum age of the file. Defaults to
            the configuration file's value.
        max_size (Union[int, None]): The maximum size of accepted files.
            Defaults to the configuration file's value.

    Returns:
        int: The number of days that the file should be retained for.
    """
    if min_age is None:
        min_age = settings.uploads.min_age
    if max_age is None:
        max_age = settings.uploads.max_age
    if max_size is None:
        max_size = settings.uploads.max_size

    if file_size > max_size or file_size < 0:
        return -1

    result = (min_age + (-max_age + min_age) *
              math.pow((file_size / max_size - 1), 3))
    return math.floor(result)
