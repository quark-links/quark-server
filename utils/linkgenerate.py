"""Link generation."""
import secrets

WORD_LISTS = ("words/1.txt", "words/2.txt")


def generate_link(separator: str = ".") -> str:
    """Generate a short link.

    Args:
        separator (str, optional): The separator character between the words.
            Defaults to ".".

    Returns:
        str: The generated link.
    """
    output = []

    for word_list in WORD_LISTS:
        with open(word_list, "r") as file:
            words = file.readlines()
            output.append(secrets.choice(words).strip())

    return separator.join(output)


if __name__ == "__main__":
    print(generate_link())
