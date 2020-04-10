"""Functions for generating and verifying API keys."""
from db import User, db
from binascii import hexlify
import os
import re


def _generate_api_key():
    return hexlify(os.urandom(32)).decode()


def _is_api_key(s):
    return re.fullmatch(r"^[0-9a-f]{64}$", s or "") is not None


def generate_api_key(user: User):
    """Generate a new API key for a user.

    Args:
        user (User): The user to generate the API key for.

    Returns:
        str: The generated API key.
    """
    api_key = _generate_api_key()
    user.api_key = api_key
    db.session.add(user)
    db.session.commit()

    return api_key


def verify_api_key(api_key: str):
    """Verify a user's API key.

    Args:
        api_key (str): The API key to verify.

    Returns:
        User: The user that the API key belongs to.
    """
    if not _is_api_key(api_key):
        return None

    user = User.query.filter_by(api_key=api_key).first()

    return user
