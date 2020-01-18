"""Utility for calculating file retention."""

import config
import math


def calculate(file_size):
    """Calculate the file retention for a specified file size.

    Args:
        file_size (int): The size of the file in Mb.

    Returns:
        int: The number of days that the file should be retained for.
    """
    min_age = config.UPLOAD_MIN_AGE
    max_age = config.UPLOAD_MAX_AGE
    max_size = config.UPLOAD_MAX_SIZE

    if file_size > max_size or file_size < 0:
        return -1

    result = (min_age + (-max_age + min_age) *
              math.pow((file_size / max_size - 1), 3))
    return math.floor(result)
