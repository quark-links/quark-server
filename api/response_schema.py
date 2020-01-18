"""A file containing the response schemas.

This file contains Marshmallow schema for each of the API responses.
"""

from flask_marshmallow import Marshmallow
from db import ShortLink, Url, Paste, Upload

ma = Marshmallow()


class ShortLinkSchema(ma.ModelSchema):
    """Marshmallow schema for short link objects."""
    class Meta:
        """Metadata about the schema."""
        fields = ("created", "updated", "link")
        model = ShortLink

    # Create a link property that is the link() function on the short link
    # object
    link = ma.Function(lambda x: x.link())


class UrlSchema(ma.ModelSchema):
    """Marshmallow schema for URL objects."""
    class Meta:
        """Metadata about the schema."""
        fields = ("url", "short_link")
        model = Url

    short_link = ma.Nested(ShortLinkSchema)


class PasteSchema(ma.ModelSchema):
    """Marshmallow schema for paste objects."""
    class Meta:
        """Metadata about the schema."""
        fields = ("language", "code", "short_link")
        model = Paste

    short_link = ma.Nested(ShortLinkSchema)


class UploadSchema(ma.ModelSchema):
    """Marshmallow schema for upload objects."""
    class Meta:
        """Metadata about the schema."""
        fields = ("mimetype", "original_filename", "short_link", "expires")
        model = Upload

    short_link = ma.Nested(ShortLinkSchema)


short_link_schema = ShortLinkSchema()
short_links_schema = ShortLinkSchema(many=True)
url_schema = UrlSchema()
urls_schema = UrlSchema(many=True)
paste_schema = PasteSchema()
pastes_schema = PasteSchema(many=True)
upload_schema = UploadSchema()
uploads_schema = UploadSchema(many=True)
