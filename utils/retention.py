"""Retention methods."""
import math
from config import settings


def calculate_retention(file_size: int) -> int:
    """Calculate the file retention for a specified file size.

    Args:
        file_size (int): The size of the file in Mb.

    Returns:
        int: The number of days that the file should be retained for.
    """
    min_age = settings.uploads.min_age
    max_age = settings.uploads.max_age
    max_size = settings.uploads.max_size

    if file_size > max_size or file_size < 0:
        return -1

    result = (min_age + (-max_age + min_age) *
              math.pow((file_size / max_size - 1), 3))
    return math.floor(result)
