"""Link generation."""
import secrets

WORD_LIST = "words.txt"


def generate_link(length=2, separator=".") -> str:
    """Generate a short link.

    Args:
        length (int, optional): The number of words long that the link should
            be. Defaults to 2.
        separator (str, optional): The separator character between the words.
            Defaults to ".".

    Returns:
        str: The generated link.
    """
    output = []

    with open(WORD_LIST, "r") as file:
        words = file.readlines()

        for i in range(length):
            output.append(secrets.choice(words).strip())

    return separator.join(output)


if __name__ == "__main__":
    print(generate_link())
