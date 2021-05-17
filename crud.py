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
from typing import IO, Optional, Union
from url_normalize import url_normalize
from utils.linkgenerate import generate_link
import datetime
from typing import Dict


def create_short_link(db: Session, user: Optional[schemas.User] = None
                      ) -> models.ShortLink:
    """Create a new short link.

    Args:
        db (Session): A database instance.
        user (Optional[schemas.User], optional): The user that has created the
            short link. Defaults to None.

    Returns:
        models.ShortLink: The created short link.
    """
    link = None

    while True:
        link = generate_link()

        conflict = db.query(models.ShortLink).filter(
            models.ShortLink.link == link).first()

        if conflict is None:
            break

    db_short_link = models.ShortLink(link=link)
    db_short_link.user = user
    return db_short_link


def create_shorten(db: Session, url: schemas.Url,
                   user: Optional[schemas.User] = None) -> models.ShortLink:
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
    db_short_link = create_short_link(db=db, user=user)
    db_short_link.url = db_url

    db.add(db_url)
    db.add(db_short_link)
    db.commit()
    db.refresh(db_short_link)
    return db_short_link


def create_paste(db: Session, paste: schemas.PasteCreate,
                 user: Optional[schemas.User] = None) -> models.ShortLink:
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
    db_short_link = create_short_link(db=db, user=user)
    db_short_link.paste = db_paste

    db.add(db_paste)
    db.add(db_short_link)
    db.commit()
    db.refresh(db_short_link)
    return db_short_link


def create_upload(db: Session, filename: str,
                  file: Union[SpooledTemporaryFile, IO], mimetype: str,
                  user: Optional[schemas.User] = None) -> models.ShortLink:
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

    file_size = os.fstat(file.fileno()).st_size / 1e+6
    retention = calculate_retention(file_size)

    if retention < 0:
        raise HTTPException(status_code=413,
                            detail="Uploaded file is too large")

    # Find conflicts that can be send instead
    conflict = db.query(models.Upload).filter(
            models.Upload.hash == file_hash,
            models.Upload.short_link.has(user=user)).first()

    if conflict is not None and conflict.short_link is not None:
        # Resave file and reset retention if properly expired
        if conflict.filename is None:
            save_upload(file, new_filename)
            conflict.filename = new_filename

        if conflict.short_link.expiry <= datetime.datetime.utcnow():
            conflict.short_link.set_expiry_days(retention)

        db.add(conflict)
        db.add(conflict.short_link)
        db.commit()
        db.refresh(conflict)

        return conflict.short_link

    db_upload = models.Upload(original_filename=filename, mimetype=mimetype,
                              filename=new_filename, file_hash=file_hash)
    db_short_link = create_short_link(db=db, user=user)
    db_short_link.upload = db_upload
    db_short_link.set_expiry_days(retention)

    save_upload(file, new_filename)

    db.add(db_upload)
    db.add(db_short_link)
    db.commit()
    db.refresh(db_short_link)
    return db_short_link


def get_short_link(db: Session, link: str) -> models.ShortLink:
    """Get a short link by it's ID.

    Args:
        db (Session): A database instance.
        link (str): The link of the short link to find.

    Returns:
        ShortLink: The short link.
    """
    return db.query(models.ShortLink).filter(
        models.ShortLink.link == link).first()


def get_or_create_user(db: Session, sub: str) -> models.User:
    """Get a user from their sub value and make one if they don't exist.

    Args:
        db (Session): A database instance.
        sub (str): The user's sub value.

    Returns:
        models.User: The user.
    """
    result = db.query(models.User).filter(models.User.sub == sub).first()

    if result is not None:
        return result

    db_user = models.User(sub)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> models.User:
    """Get a user by it's ID.

    Args:
        db (Session): A database instance.
        user_id (int): The ID of the user to find.

    Returns:
        User: The user.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_links(db: Session, user_id: int) -> models.ShortLink:
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


def get_stats(db: Session) -> Dict[str, int]:
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


def bucket_create(db: Session, user: models.User) -> models.Bucket:
    """Create a new bucket.

    Args:
        db (Session): A database instance.
        user (models.User): The owner of the new bucket.

    Returns:
        models.Bucket: The created bucket.
    """
    name = None

    while True:
        name = generate_link()

        conflict = db.query(models.Bucket).filter(
            models.Bucket.name == name).first()

        if conflict is None:
            break

    db_bucket = models.Bucket(name, user)

    db.add(db_bucket)
    db.commit()
    db.refresh(db_bucket)
    return db_bucket


def bucket_get(db: Session, name: str, user: models.User,
               check_owner: bool = True) -> models.Bucket:
    """Get an existing bucket by name.

    Args:
        db (Session): The database instance.
        name (str): The name of the bucket to get.
        user (models.User): The user that is requesting the bucket.
        check_owner (bool, optional): Whether to check the owner of the bucket.
            Defaults to True.

    Returns:
        models.Bucket: The bucket.
    """
    db_bucket = db.query(models.Bucket).filter(
        models.Bucket.name == name).first()

    not_found_exception = HTTPException(status_code=404,
                                        detail="Bucket not found")

    if db_bucket is None:
        raise not_found_exception

    if check_owner:
        if db_bucket.user != user:
            raise not_found_exception
    else:
        if not db_bucket.public and db_bucket.user != user:
            raise not_found_exception

    return db_bucket


def bucket_delete(db: Session, name: str, user: models.User) -> None:
    """Delete a bucket by name.

    Args:
        db (Session): The database instance.
        name (str): The name of the bucket to delete.
        user (models.User): The user that is deleting the bucket.
    """
    db_bucket = bucket_get(db, name, user)
    db.delete(db_bucket)
    db.commit()


def bucket_add(db: Session, short_link: str, bucket_name: str,
               user: models.User) -> models.Bucket:
    """Add a short link to a bucket.

    Args:
        db (Session): The database instance.
        short_link (str): The short link to add.
        bucket_name (str): The bucket to add to.
        user (models.User): The user that is requesting.

    Returns:
        models.Bucket: The updated bucket.
    """
    db_short_link = db.query(models.ShortLink).filter(
        models.ShortLink.link == short_link).first()
    db_bucket = bucket_get(db, bucket_name, user)

    if db_short_link is None:
        raise HTTPException(status_code=400,
                            detail="Invalid short link")

    if db_short_link.user != user:
        raise HTTPException(status_code=401,
                            detail="You are not the owner of the short link")

    db_short_link.bucket = db_bucket
    db.commit()
    db.refresh(db_bucket)
    return db_bucket


def bucket_remove(db: Session, short_link: str, bucket_name: str,
                  user: models.User) -> models.Bucket:
    """Remove a short link to a bucket.

    Args:
        db (Session): The database instance.
        short_link (str): The short link to remove.
        bucket_name (str): The bucket to remove from.
        user (models.User): The user that is requesting.

    Returns:
        models.Bucket: The updated bucket.
    """
    db_short_link = db.query(models.ShortLink).filter(
        models.ShortLink.link == short_link).first()
    db_bucket = bucket_get(db, bucket_name, user)

    if db_short_link is None:
        raise HTTPException(status_code=400,
                            detail="Invalid short link")

    if db_short_link.user != user:
        raise HTTPException(status_code=401,
                            detail="You are not the owner of the short link")

    db_short_link.bucket = None
    db.commit()
    db.refresh(db_bucket)
    return db_bucket
