"""Utility for the different paste languages."""

import json


languages = json.load(open("utils/languages.json", "r"))


def language_list():
    """Get a list of all of the available language IDs.

    Returns:
        list[dict]: The list of langauge objects
    """
    return [lang["id"] for lang in languages]


def get_language_by_id(lang_id):
    """Get a language dictionary from a language ID.

    Args:
        lang_id (str): The language ID to search for

    Returns:
        dict: The language object
    """
    return next((lang for lang in languages if lang["id"] == lang_id), None)
