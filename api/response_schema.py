from flask_marshmallow import Marshmallow
from db import ShortLink, Url, Paste, Upload

ma = Marshmallow()


class ShortLinkSchema(ma.ModelSchema):
    class Meta:
        fields = ("created", "updated", "link")
        model = ShortLink

    link = ma.Function(lambda x: x.link())


class UrlSchema(ma.ModelSchema):
    class Meta:
        fields = ("url", "short_link")
        model = Url
    
    short_link = ma.Nested(ShortLinkSchema)


class PasteSchema(ma.ModelSchema):
    class Meta:
        fields = ("language", "code", "short_link")
        model = Paste

    short_link = ma.Nested(ShortLinkSchema)


class UploadSchema(ma.ModelSchema):
    class Meta:
        fields = ("mimetype", "original_filename", "short_link")
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
