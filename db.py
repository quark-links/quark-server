"""A file for containing all of the database specific code for VH7.

This file contains SQLAlchemy models for each of the different things that are
stored in the database.
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from hashids import Hashids
import config
import datetime
from passlib.hash import pbkdf2_sha256
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
import utils.languages as lang

metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })
Base = declarative_base(metadata=metadata)

db = SQLAlchemy(model_class=Base)
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
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(),
                        nullable=False)
    updated = db.Column(db.DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)
    url = db.relationship("Url", uselist=False,
                          back_populates="short_link")
    paste = db.relationship("Paste", uselist=False,
                            back_populates="short_link")
    upload = db.relationship("Upload", uselist=False,
                             back_populates="short_link")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="short_links")

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

    def get_type(self):
        """Get the type of short link.

        Returns:
            str: The type of short link: 'url', 'paste', 'upload' or None.
        """
        if self.url is not None:
            return "url"
        if self.paste is not None:
            return "paste"
        if self.upload is not None:
            return "upload"


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

    def language_info(self):
        """Get all of the language information for the paste's language.

        Returns:
            dict: Dictionary containing language information such as id, name
                and file extension.
        """
        return lang.get_language_by_id(self.language)


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


class User(db.Model):
    """SQLAlchemy model for users.

    This is for storing the information for a specific user.
    """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(),
                        nullable=False)
    updated = db.Column(db.DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)
    email = db.Column(db.String(100), nullable=True, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(400), nullable=False)
    authenticated = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    short_links = db.relationship("ShortLink", back_populates="user")
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime(timezone=True), nullable=True)
    confirm_token = db.Column(db.String(20), nullable=True)
    reset_token = db.Column(db.String(20), nullable=True)

    def __init__(self, username, email):
        """Create a new user object.

        Args:
            username (str): The desired username.
            email (str): The email of the user.
        """
        self.username = username
        self.email = email

    def set_password(self, password):
        """Hash and then set a password for the user.

        Args:
            password (str): The plain-text password for the user.
        """
        password_hash = pbkdf2_sha256.hash(password)
        self.password = password_hash

    def verify_password(self, password):
        """Verify a password against the user's stored hash.

        Args:
            password (str): The plain-text password to verify.

        Returns:
            bool: True if the password is correct, False if not.
        """
        return pbkdf2_sha256.verify(password, self.password)

    @property
    def is_authenticated(self):
        """Whether the user has been authenticated or not.

        Required by flask-login.
        """
        return self.authenticated

    @property
    def is_active(self):
        """Whether the user is active or not.

        Inactive users aren't allowed to login. Required by flask-login.
        """
        return self.active and self.confirmed

    @property
    def is_anonymous(self):
        """Whether the user is anonymous (i.e. doesn't require a password to login).

        No users are anonymous so it is hard-set to False. Required by
        flask-login.
        """
        return False

    def get_id(self):
        """Get the user's ID.

        Required by flask-login.
        """
        return str(self.id)

    def clear_tokens(self):
        """Remove the confirm and reset tokens so that they can't be reused."""
        self.confirm_token = None
        self.reset_token = None
