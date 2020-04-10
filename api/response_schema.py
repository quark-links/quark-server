"""A file containing the response schemas.

This file contains Marshmallow schema for each of the API responses.
"""

from flask_marshmallow import Marshmallow
from marshmallow import post_dump
from db import ShortLink, Url, Paste, Upload, User

ma = Marshmallow()


class UrlSchema(ma.ModelSchema):
    """Marshmallow schema for URL objects."""
    class Meta:
        """Metadata about the schema."""
        fields = ("url",)
        model = Url


class PasteSchema(ma.ModelSchema):
    """Marshmallow schema for paste objects."""
    class Meta:
        """Metadata about the schema."""
        fields = ("language", "code")
        model = Paste


class UploadSchema(ma.ModelSchema):
    """Marshmallow schema for upload objects."""
    class Meta:
        """Metadata about the schema."""
        fields = ("mimetype", "original_filename", "expires")
        model = Upload


class ShortLinkSchema(ma.ModelSchema):
    """Marshmallow schema for short link objects."""
    class Meta:
        """Metadata about the schema."""
        fields = ("created", "updated", "link", "url", "paste", "upload",
                  "type")
        model = ShortLink

    @post_dump(pass_many=False)
    def remove_null_values(self, data, many):
        """Function to clean up null values from the dumped data.

        Args:
            data (dict): The dumped data to be cleaned.
            many (bool): Whether there are many items of data in the dump.

        Returns:
            dict: The cleaned up data.
        """
        # If there is no value for the url, remove it
        if data["url"] is None:
            del data["url"]
        # If there is no value for the paste, remove it
        if data["paste"] is None:
            del data["paste"]
        # If there is no value for the upload, remove it
        if data["upload"] is None:
            del data["upload"]
        return data

    # Create a link property that is the link() function on the short link
    # object
    link = ma.Function(lambda x: x.link())
    type = ma.Function(lambda x: x.get_type())
    url = ma.Nested(UrlSchema, skip_missing=True)
    paste = ma.Nested(PasteSchema, skip_missing=True)
    upload = ma.Nested(UploadSchema, skip_missing=True)


class UserSchema(ma.ModelSchema):
    """Marshmallow schema for user objects."""
    class Meta:
        """Metadata about the schema."""
        fields = ("created", "updated", "email", "username", "confirmed",
                  "confirmed_on")
        model = User


short_link_schema = ShortLinkSchema()
short_links_schema = ShortLinkSchema(many=True)
url_schema = UrlSchema()
urls_schema = UrlSchema(many=True)
paste_schema = PasteSchema()
pastes_schema = PasteSchema(many=True)
upload_schema = UploadSchema()
uploads_schema = UploadSchema(many=True)
user_schema = UserSchema()
