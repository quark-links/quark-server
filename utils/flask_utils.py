"""Module containing Flask utilities."""

from urllib.parse import urlparse, urljoin
from flask import request


def is_safe_url(target):
    """Check a URL to see if it is safe to redirect a user to.

    Args:
        target (str): The URL that needs to be tested.

    Returns:
        bool: True if the URL is safe to redirect to, False if it is not.
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (test_url.scheme in ("http", "https") and
            ref_url.netloc == test_url.netloc)
