from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from hashids import Hashids

db = SQLAlchemy()
hashids = Hashids(min_length=0, alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", salt="YeCqDt4fStm8DffjXQunuvcU3fFGBK9t")


class ShortLink(db.Model):
    __tablename__ = "shortlink"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    creator_ip = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(2048), nullable=False)

    def __init__(self, creator_ip, url):
        self.creator_ip = creator_ip

    def short_link(self):
        return "/" + hashids.encode(self.id)