from flask_marshmallow import Marshmallow
from db import ShortLink, LongUrl

ma = Marshmallow()


class LongUrlSchema(ma.ModelSchema):
    class Meta:
        fields = ("url",)
        model = LongUrl


class ShortLinkSchema(ma.ModelSchema):
    class Meta:
        fields = ("created", "updated", "longurl", "shortlink")
        model = ShortLink

    longurl = ma.Nested(LongUrlSchema)
    shortlink = ma.Function(lambda obj: obj.url())


shortlink_schema = ShortLinkSchema()
shortlinks_schema = ShortLinkSchema(many=True)
longurl_schema = LongUrlSchema()
longurls_schema = LongUrlSchema(many=True)