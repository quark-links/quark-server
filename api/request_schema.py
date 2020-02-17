"""A file containing the request schemas.

This file contains webargs schema for each of the API requests.
"""

from webargs import fields

_valid_languages = ["apache", "bash", "coffeescript", "cpp", "cs", "css", "diff", "go", "http", "ini", "java", "javascript", "json", "kotlin", "less", "lua", "makefile", "xml", "markdown", "nginx", "objectivec", "perl", "php", "plaintext", "properties", "python", "ruby", "rust", "scss", "shell", "sql", "swift", "typescript", "yaml"]


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
