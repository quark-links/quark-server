"""A file containing all of the Flask routes for the API."""

from flask import Blueprint, request, current_app, jsonify
from url_normalize import url_normalize
from webargs.flaskparser import use_args
from api.request_schema import url_args, paste_args, upload_args
from api.response_schema import url_schema, paste_schema, upload_schema
import uuid
import os
import hashlib
import utils.retention as retention

from db import db, ShortLink, Url, Paste, Upload

api = Blueprint("api", __name__, url_prefix="/api")


def _get_ip():
    return request.environ.get("HTTP_X_REAL_IP", request.remote_addr)


@api.route("/shorten", methods=["POST"])
@use_args(url_args)
def shorten(args):
    """A flask route for shortening URLs."""
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
    """A flask route for creating pastes."""
    req_code = args["code"].strip()
    # Calculate a hash of the text
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
    """A flask route for uploading files."""
    # Create a filename for the uploaded file
    filename = str(uuid.uuid4())
    req_file = args["file"]
    req_filename = req_file.filename
    req_mimetype = req_file.mimetype
    # Calculate a hash of the uploaded file
    req_hash = hashlib.sha256(req_file.read()).hexdigest()

    # Reset the file to the beginning (otherwise the saved file is empty)
    req_file.seek(0)

    # Calculate file size of uploaded file in Mb
    file_size = os.fstat(req_file.fileno()).st_size / 1e+6

    duplicate = Upload.query.filter_by(hash=req_hash).first()
    # If the uploaded file already exists
    if duplicate is not None:
        # If the uploaded file has expired
        if duplicate.filename is None:
            ret = retention.calculate(file_size)

            if ret < 0:
                raise Exception("The uploaded file was over the maximum size!")

            duplicate.filename = filename
            duplicate.set_retention(ret)

            req_file.save(os.path.join(current_app.config["UPLOAD_FOLDER"],
                                       filename))

            db.session.commit()

        return upload_schema.jsonify(duplicate)
    else:
        ret = retention.calculate(file_size)

        if ret < 0:
            raise Exception("The uploaded file was over the maximum size!")

        upload = Upload(req_filename, req_mimetype, filename, req_hash, ret)
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
    """A flask error handler for creating pretty JSON error responses."""
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])

    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code
