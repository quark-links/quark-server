"""A file containing the request schemas.

This file contains webargs schema for each of the API requests.
"""

from webargs import fields

_valid_languages = ["plain"]


url_args = {
    "url": fields.Url(required=True)
}

paste_args = {
    "code": fields.Str(required=True,
                       validate=lambda c: bool(c.strip())),
    "language": fields.Str(required=True,
                           validate=lambda l: l in _valid_languages)
}

upload_args = {
    "file": fields.Field(location="files", required=True)
}
