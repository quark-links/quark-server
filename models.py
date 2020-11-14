from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime

from database import Base, hashids


class ShortLink(Base):
    __tablename__ = "shortlink"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now(),
                     nullable=False)
    updated = Column(DateTime(timezone=True), server_default=func.now(),
                     onupdate=func.now(), nullable=False)
    url = relationship("Url", uselist=False,
                       back_populates="short_link")
    paste = relationship("Paste", uselist=False,
                         back_populates="short_link")
    upload = relationship("Upload", uselist=False,
                          back_populates="short_link")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="short_links")

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


class Url(Base):
    __tablename__ = "url"

    id = Column(Integer, primary_key=True)
    short_link_id = Column(Integer, ForeignKey("shortlink.id"))
    short_link = relationship("ShortLink", back_populates="url")
    url = Column(String(2048), nullable=False)

    def __init__(self, url):
        """Create a new URL object.

        Args:
            url (str): The URL.
        """
        self.url = url


class Paste(Base):
    __tablename__ = "paste"

    id = Column(Integer, primary_key=True)
    short_link_id = Column(Integer, ForeignKey("shortlink.id"))
    short_link = relationship("ShortLink", back_populates="paste")
    language = Column(String(100), nullable=False)
    code = Column(Text(), nullable=False)
    hash = Column(String(64), nullable=False)

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


class Upload(Base):
    __tablename__ = "upload"

    id = Column(Integer, primary_key=True)
    short_link_id = Column(Integer, ForeignKey("shortlink.id"))
    short_link = relationship("ShortLink", back_populates="upload")
    mimetype = Column(String(100), nullable=False)
    original_filename = Column(String(400), nullable=False)
    filename = Column(String(400), nullable=True)
    hash = Column(String(64), nullable=False)
    expires = Column(DateTime(timezone=True), nullable=False)

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


class User(Base):
    """SQLAlchemy model for users.
    This is for storing the information for a specific user.
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now(),
                     nullable=False)
    updated = Column(DateTime(timezone=True), server_default=func.now(),
                     onupdate=func.now(), nullable=False)
    email = Column(String(100), nullable=True, unique=True)
    name = Column(String(50), nullable=True)
    password = Column(String(400), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    short_links = relationship("ShortLink", back_populates="user")
    confirmed = Column(Boolean, nullable=False, default=False)
    confirmed_on = Column(DateTime(timezone=True), nullable=True)
    confirm_token = Column(String(100), nullable=True)
    reset_token = Column(String(100), nullable=True)
    api_key = Column(String(100), nullable=True)

    def __init__(self, email, password):
        """Create a new user object.
        Args:
            username (str): The desired username.
            email (str): The email of the user.
        """
        self.email = email
        self.password = password
