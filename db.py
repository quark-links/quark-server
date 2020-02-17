"""A file for containing all of the database specific code for VH7.

This file contains SQLAlchemy models for each of the different things that are
stored in the database.
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from hashids import Hashids
import config
import datetime

db = SQLAlchemy()
# Create a new hashids instance for converting database IDs to short links
hashids = Hashids(min_length=0,
                  alphabet=config.HASHIDS_ALPHABET,
                  salt=config.HASHIDS_SALT)


class ShortLink(db.Model):
    """SQLAlchemy model for short links.

    This is for storing a short link and pointing it to either a URL, paste or
    upload. It also stores some metadata about the time and who created it.
    """
    __tablename__ = "shortlink"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now())
    creator_ip = db.Column(db.String(50), nullable=False)
    url = db.relationship("Url", uselist=False,
                          back_populates="short_link")
    paste = db.relationship("Paste", uselist=False,
                            back_populates="short_link")
    upload = db.relationship("Upload", uselist=False,
                             back_populates="short_link")

    def __init__(self, creator_ip):
        """Create a new short link object.

        Args:
            creator_ip (str): The IP of the user who created the short link.
        """
        self.creator_ip = creator_ip

    def link(self, leading_slash=True):
        """Get the short link.

        The output of this should be added to the end of the instance URL.

        Args:
            leading_slash (bool, optional): Add a leading slash to the
                beginning of the short link. Defaults to True.

        Returns:
            str: The short link.
        """
        return ("/" if leading_slash else "") + hashids.encode(self.id)


class Url(db.Model):
    """SQLAlchemy model for URLs.

    This is for storing a specific URL which is then pointed to a short link.
    """
    __tablename__ = "url"

    id = db.Column(db.Integer, primary_key=True)
    short_link_id = db.Column(db.Integer, db.ForeignKey("shortlink.id"))
    short_link = db.relationship("ShortLink", back_populates="url")
    url = db.Column(db.String(2048), nullable=False)

    def __init__(self, url):
        """Create a new URL object.

        Args:
            url (str): The URL.
        """
        self.url = url


class Paste(db.Model):
    """SQLAlchemy model for pastes.

    This is for storing a paste (i.e. a chunk of text) which is then pointed
    to a short link.
    """
    __tablename__ = "paste"

    id = db.Column(db.Integer, primary_key=True)
    short_link_id = db.Column(db.Integer, db.ForeignKey("shortlink.id"))
    short_link = db.relationship("ShortLink", back_populates="paste")
    language = db.Column(db.String(100), nullable=False)
    code = db.Column(db.TEXT(), nullable=False)
    hash = db.Column(db.String(64), nullable=False)

    def __init__(self, code, language, hash):
        """Create a new paste object.

        Args:
            code (str): The chunk of text to be stored.
            language (str): The programming language that the paste is written
                in.
            hash (str): A SHA256 hash of the `code`.
        """
        self.code = code
        self.language = language
        self.hash = hash


class Upload(db.Model):
    """SQLAlchemy model for uploads.

    This is for storing metadata about uploaded files which is then pointed to
    a short link. This doesn't actually store the file but stores where it is
    saved along with the file's mimetype.
    """
    __tablename__ = "upload"

    id = db.Column(db.Integer, primary_key=True)
    short_link_id = db.Column(db.Integer, db.ForeignKey("shortlink.id"))
    short_link = db.relationship("ShortLink", back_populates="upload")
    mimetype = db.Column(db.String(100), nullable=False)
    original_filename = db.Column(db.String(400), nullable=False)
    filename = db.Column(db.String(400), nullable=True)
    hash = db.Column(db.String(64), nullable=False)
    expires = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, original_filename, mimetype, filename, hash, retention):
        """Create a new upload object.

        Args:
            original_filename (str): The original filename of the uploaded
                file.
            mimetype (str): The MIME type of the uploaded file.
            filename (str): The filename of the uploaded file on the server.
            hash (str): A SHA256 hash of the uploaded file.
            retention (int): The number of days until the file expires.
        """
        self.original_filename = original_filename
        self.mimetype = mimetype
        self.filename = filename
        self.hash = hash
        self.set_retention(retention)

    def set_retention(self, days):
        """Set the expiry date to now plus the specified number of days.

        Args:
            days (int): The number of days that the file should be kept for.
        """
        self.expires = datetime.datetime.now() + datetime.timedelta(days=days)
