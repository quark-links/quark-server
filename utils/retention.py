import math
import os


def calculate_retention(file_size):
    """Calculate the file retention for a specified file size.
    Args:
        file_size (int): The size of the file in Mb.
    Returns:
        int: The number of days that the file should be retained for.
    """
    min_age = os.getenv("UPLOAD_MIN_AGE", 30)
    max_age = os.getenv("UPLOAD_MAX_AGE", 90)
    max_size = os.getenv("UPLOAD_MAX_SIZE", 256)

    if file_size > max_size or file_size < 0:
        return -1

    result = (min_age + (-max_age + min_age) *
              math.pow((file_size / max_size - 1), 3))
    return math.floor(result)
