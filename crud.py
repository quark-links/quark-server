from sqlalchemy.orm import Session
import models
import schemas
import hashlib
import uuid
from tempfile import SpooledTemporaryFile
import os
from utils.retention import calculate_retention
from fastapi import HTTPException
from utils.uploads import save_upload
from passlib.hash import pbkdf2_sha256
from typing import Optional


def create_shorten(db: Session, url: schemas.Url,
                   user: Optional[schemas.User] = None):
    db_url = models.Url(url=url.url)
    db_short_link = models.ShortLink()
    db_short_link.url = db_url

    if user is not None:
        db_short_link.user = user

    db.add(db_url)
    db.add(db_short_link)
    db.commit()
    db.refresh(db_short_link)
    return db_short_link


def create_paste(db: Session, paste: schemas.PasteCreate,
                 user: Optional[schemas.User] = None):
    code_hash = hashlib.sha256(paste.code.encode("utf8")).hexdigest()
    db_paste = models.Paste(code=paste.code, language=paste.language,
                            hash=code_hash)
    db_short_link = models.ShortLink()
    db_short_link.paste = db_paste

    if user is not None:
        db_short_link.user = user

    db.add(db_paste)
    db.add(db_short_link)
    db.commit()
    db.refresh(db_short_link)
    return db_short_link


def create_upload(db: Session, filename: str, file: SpooledTemporaryFile,
                  mimetype: str, user: Optional[schemas.User] = None):
    new_filename = str(uuid.uuid4())
    file_hash = hashlib.sha256(file.read()).hexdigest()

    # Reset the file back to the beginning
    file.seek(0)

    file_size = os.fstat(file.fileno()).st_size / 1e+6
    retention = calculate_retention(file_size)

    if retention < 0:
        raise HTTPException(status_code=413,
                            detail="Uploaded file is too large")

    db_upload = models.Upload(original_filename=filename, mimetype=mimetype,
                              filename=new_filename, hash=file_hash,
                              retention=retention)
    db_short_link = models.ShortLink()
    db_short_link.upload = db_upload

    if user is not None:
        db_short_link.user = user

    save_upload(file, new_filename)

    db.add(db_upload)
    db.add(db_short_link)
    db.commit()
    db.refresh(db_short_link)
    return db_short_link


def get_short_link(db: Session, short_link_id: int):
    return db.query(models.ShortLink).filter(
        models.ShortLink.id == short_link_id).first()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_links(db: Session, user_id: int):
    return db.query(models.ShortLink).filter(models.ShortLink.user_id == user_id).order_by(models.ShortLink.created.desc()).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pbkdf2_sha256.hash(user.password)
    db_user = models.User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
