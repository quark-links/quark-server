from flask import Blueprint, request
from url_normalize import url_normalize

from db import db, ShortLink, LongUrl
from api.request_schema import CreateShortLinkSchema, CreateUploadSchema
from api.response_schema import ma, shortlink_schema, shortlinks_schema, longurl_schema, longurls_schema

api = Blueprint("api", __name__, url_prefix="/api")

ma.init_app(api)


@api.route("/shorten", methods=["POST"])
def shorten():
    errors = CreateShortLinkSchema().validate(request.form)
    if errors:
        return str(errors)

    url = url_normalize(request.form["url"])

    duplicate_longurl = LongUrl.query.filter_by(url=url).first()
    if duplicate_longurl is not None:
        print("Using existing")
        return shortlink_schema.jsonify(duplicate_longurl.shortlink)
    else:
        print("Creating new")
        shortlink = ShortLink(request.remote_addr, url)
        db.session.add(shortlink)
        db.session.commit()

        return shortlink_schema.jsonify(shortlink)