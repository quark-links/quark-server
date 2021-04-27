"""Retention methods."""
import math
import os
from typing import Union


def calculate_retention(file_size: int, min_age: Union[int, None] = None,
                        max_age: Union[int, None] = None,
                        max_size: Union[int, None] = None) -> int:
    """Calculate the file retention for a specified file size.

    Args:
        file_size (int): The size of the file in Mb.

    Returns:
        int: The number of days that the file should be retained for.
    """
    if min_age is None:
        min_age = int(os.getenv("UPLOAD_MIN_AGE", "30"))

    if max_age is None:
        max_age = int(os.getenv("UPLOAD_MAX_AGE", "90"))

    if max_size is None:
        max_size = int(os.getenv("UPLOAD_MAX_SIZE", "256"))

    if file_size > max_size or file_size < 0:
        return -1

    result = (min_age + (-max_age + min_age) *
              math.pow((file_size / max_size - 1), 3))
    return math.floor(result)
