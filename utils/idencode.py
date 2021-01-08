"""Methods for encoding IDs."""
from os import getenv

ALPHABET = list(getenv("ID_ALPHABET", ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKL"
                                       "MNOPQRSTUVWXYZ0123456789")))


def encode(n: int) -> str:
    """Encode a given ID into a string.

    Args:
        n (int): The ID to encode.

    Returns:
        str: The encoded ID.
    """
    if n == 0:
        return ALPHABET[0]
    arr = []
    base = len(ALPHABET)
    while n:
        n, remainder = divmod(n, base)
        arr.append(ALPHABET[remainder])
    arr.reverse()
    return ''.join(arr)


def decode(encoded_id: str) -> int:
    """Decode a given string into an ID.

    Args:
        encoded_id (str): The string to decode.

    Returns:
        int: The decoded ID.
    """
    base = len(ALPHABET)
    length = len(encoded_id)
    n = 0

    idx = 0
    for c in encoded_id:
        power = (length - (idx + 1))
        n += ALPHABET.index(c) * (base ** power)
        idx += 1

    return n
