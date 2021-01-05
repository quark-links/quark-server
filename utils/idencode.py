ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def encode(n: int) -> str:
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
    base = len(ALPHABET)
    length = len(encoded_id)
    n = 0

    idx = 0
    for c in encoded_id:
        power = (length - (idx + 1))
        n += ALPHABET.index(c) * (base ** power)
        idx += 1

    return n
