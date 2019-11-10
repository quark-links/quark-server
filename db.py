from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from hashids import Hashids

db = SQLAlchemy()
hashids = Hashids(min_length=0, alphabet=("abcdefghijklmnopqrstuvwxyzABCDEFGHI"
                                          "JKLMNOPQRSTUVWXYZ0123456789"),
                  salt="YeCqDt4fStm8DffjXQunuvcU3fFGBK9t")


class ShortLink(db.Model):
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
        self.creator_ip = creator_ip

    def link(self):
        return "/" + hashids.encode(self.id)


class Url(db.Model):
    __tablename__ = "url"

    id = db.Column(db.Integer, primary_key=True)
    short_link_id = db.Column(db.Integer, db.ForeignKey("shortlink.id"))
    short_link = db.relationship("ShortLink", back_populates="url")
    url = db.Column(db.String(2048), nullable=False)

    def __init__(self, url):
        self.url = url


class Paste(db.Model):
    __tablename__ = "paste"

    id = db.Column(db.Integer, primary_key=True)
    short_link_id = db.Column(db.Integer, db.ForeignKey("shortlink.id"))
    short_link = db.relationship("ShortLink", back_populates="paste")
    language = db.Column(db.String(100), nullable=False)
    code = db.Column(db.TEXT(), nullable=False)
    hash = db.Column(db.String(64), nullable=False)

    def __init__(self, code, language, hash):
        self.code = code
        self.language = language
        self.hash = hash


class Upload(db.Model):
    __tablename__ = "upload"

    id = db.Column(db.Integer, primary_key=True)
    short_link_id = db.Column(db.Integer, db.ForeignKey("shortlink.id"))
    short_link = db.relationship("ShortLink", back_populates="upload")
    mimetype = db.Column(db.String(100), nullable=False)
    original_filename = db.Column(db.String(400), nullable=False)
    filename = db.Column(db.String(400), nullable=False)
    hash = db.Column(db.String(64), nullable=False)

    def __init__(self, original_filename, mimetype, filename, hash):
        self.original_filename = original_filename
        self.mimetype = mimetype
        self.filename = filename
        self.hash = hash
