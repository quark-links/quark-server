"""Utilities for managing paste languages."""
import json
import os

language_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "languages.json")
languages = json.load(open(language_path, "r"))
language_ids = [language["id"] for language in languages]
