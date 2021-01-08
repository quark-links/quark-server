"""Methods for performing actions with the database."""
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
from url_normalize import url_normalize


def create_shorten(db: Session, url: schemas.Url,
                   user: Optional[schemas.User] = None):
    """Create a new short URL.

    Args:
        db (Session): A database instance.
        url (schemas.Url): The URL to shorten.
        user (Optional[schemas.User], optional): The user that has created the
            short URL. Defaults to None.

    Returns:
        ShortLink: The created short link
    """
    url.url = url_normalize(url.url)

    # Find conflicts that can be send instead
    conflict = db.query(models.Url).filter(
            models.Url.url == url.url,
            models.Url.short_link.has(user=user)).first()

    if conflict is not None and conflict.short_link is not None:
        return conflict.short_link

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
    """Create a new paste.

    Args:
        db (Session): A database instance.
        paste (schemas.PasteCreate): The paste.
        user (Optional[schemas.User], optional): The user that has created the
            paste. Defaults to None.

    Returns:
        ShortLink: The created short link
    """
    code_hash = hashlib.sha256(paste.code.encode("utf8")).hexdigest()

    # Find conflicts that can be send instead
    conflict = db.query(models.Paste).filter(
            models.Paste.hash == code_hash,
            models.Paste.short_link.has(user=user)).first()

    if conflict is not None and conflict.short_link is not None:
        return conflict.short_link

    db_paste = models.Paste(code=paste.code, language=paste.language,
                            code_hash=code_hash)
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
    """Create and save an uploaded file.

    Args:
        db (Session): A database instance.
        filename (str): The original filename of the uploaded file.
        file (SpooledTemporaryFile): The file that was uploaded.
        mimetype (str): The content type of the file.
        user (Optional[schemas.User], optional): The user that has uploaded
            the file. Defaults to None.

    Raises:
        HTTPException: If the uploaded file is too large.

    Returns:
        ShortLink: The created short link.
    """
    new_filename = str(uuid.uuid4())
    file_hash = hashlib.sha256(file.read()).hexdigest()

    # Reset the file back to the beginning
    file.seek(0)

    # Find conflicts that can be send instead
    conflict = db.query(models.Upload).filter(
            models.Upload.hash == file_hash,
            models.Upload.short_link.has(user=user)).first()

    if conflict is not None and conflict.short_link is not None:
        return conflict.short_link

    file_size = os.fstat(file.fileno()).st_size / 1e+6
    retention = calculate_retention(file_size)

    if retention < 0:
        raise HTTPException(status_code=413,
                            detail="Uploaded file is too large")

    db_upload = models.Upload(original_filename=filename, mimetype=mimetype,
                              filename=new_filename, file_hash=file_hash,
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
    """Get a short link by it's ID.

    Args:
        db (Session): A database instance.
        short_link_id (int): The ID of the short link to find.

    Returns:
        ShortLink: The short link.
    """
    return db.query(models.ShortLink).filter(
        models.ShortLink.id == short_link_id).first()


def get_user(db: Session, user_id: int):
    """Get a user by it's ID.

    Args:
        db (Session): A database instance.
        user_id (int): The ID of the user to find.

    Returns:
        User: The user.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Get a user by it's email address.

    Args:
        db (Session): A database instance.
        email (str): The email of the user to find.

    Returns:
        User: The user.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_links(db: Session, user_id: int):
    """Get a given user's short links.

    Args:
        db (Session): A database instance.
        user_id (int): The ID of the user.

    Returns:
        List[ShortLinks]: The user's short links.
    """
    return db.query(models.ShortLink).filter(
        models.ShortLink.user_id == user_id).order_by(
        models.ShortLink.created.desc()).all()


def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user.

    Args:
        db (Session): A database instance.
        user (schemas.UserCreate): The user to create.

    Returns:
        User: The created user.
    """
    hashed_password = pbkdf2_sha256.hash(user.password)
    db_user = models.User(email=user.email, password=hashed_password)

    if user.name is not None and user.name.strip() != "":
        db_user.name = user.name.strip()

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: models.User, new_user: schemas.UserUpdate):
    """Update a user.

    Args:
        db (Session): A database instance.
        user (models.User): The user to update.
        new_user (schemas.UserUpdate): The information about a user to update.

    Returns:
        User: The updated user.
    """
    if new_user.name is not None and new_user.name.strip() != "":
        user.name = new_user.name

    if (new_user.email is not None and new_user.email.strip() != "" and
            user.email != new_user.email):
        user.email = new_user.email
        user.confirmed = False
        user.confirmed_on = None

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_stats(db: Session):
    """Get the current statistics.

    Args:
        db (Session): A database instance.

    Returns:
        dict: The instance's statistics.
    """
    shortens = db.query(models.Url).count()
    uploads = db.query(models.Upload).count()
    pastes = db.query(models.Paste).count()
    total = db.query(models.ShortLink).count()

    return {
        "shortened_links": shortens,
        "uploaded_files": uploads,
        "pasted_code": pastes,
        "total": total
    }
