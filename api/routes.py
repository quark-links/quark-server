from flask import Blueprint, request, current_app, jsonify
from url_normalize import url_normalize
from webargs.flaskparser import use_args
from api.request_schema import url_args, paste_args, upload_args
from api.response_schema import url_schema, paste_schema, upload_schema
import uuid
import os
import hashlib

from db import db, ShortLink, Url, Paste, Upload

api = Blueprint("api", __name__, url_prefix="/api")


def _get_ip():
    return request.environ.get("HTTP_X_REAL_IP", request.remote_addr)


@api.route("/shorten", methods=["POST"])
@use_args(url_args)
def shorten(args):
    req_url = url_normalize(args["url"])

    duplicate = Url.query.filter_by(url=req_url).first()
    if duplicate is not None:
        return url_schema.jsonify(duplicate)
    else:
        url = Url(req_url)
        short_link = ShortLink(_get_ip())
        short_link.url = url

        db.session.add(url)
        db.session.add(short_link)
        db.session.commit()

        return url_schema.jsonify(url)


@api.route("/paste", methods=["POST"])
@use_args(paste_args)
def paste(args):
    req_code = args["code"].strip()
    req_hash = hashlib.sha256(req_code.encode("utf8")).hexdigest()
    req_lang = args["language"]

    duplicate = Paste.query.filter_by(hash=req_hash).first()
    if duplicate is not None:
        return paste_schema.jsonify(duplicate)
    else:
        paste = Paste(req_code, req_lang, req_hash)
        short_link = ShortLink(_get_ip())
        short_link.paste = paste

        db.session.add(paste)
        db.session.add(short_link)
        db.session.commit()

        return paste_schema.jsonify(paste)


@api.route("/upload", methods=["POST"])
@use_args(upload_args)
def upload(args):
    filename = str(uuid.uuid4())
    req_file = args["file"]
    req_filename = req_file.filename
    req_mimetype = req_file.mimetype
    req_hash = hashlib.sha256(req_file.read()).hexdigest()
    # file_size = req_file.tell()

    # Reset the file to the beginning (otherwise the saved file is empty)
    req_file.seek(0)

    duplicate = Upload.query.filter_by(hash=req_hash).first()
    if duplicate is not None:
        return upload_schema.jsonify(duplicate)
    else:
        upload = Upload(req_filename, req_mimetype, filename, req_hash)
        short_link = ShortLink(_get_ip())
        short_link.upload = upload

        req_file.save(os.path.join(current_app.config["UPLOAD_FOLDER"],
                                   filename))

        db.session.add(upload)
        db.session.add(short_link)
        db.session.commit()

        return upload_schema.jsonify(upload)


@api.errorhandler(422)
@api.errorhandler(400)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])

    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code
