"""Pydantic schemas."""
from typing import Optional
from pydantic import BaseModel, HttpUrl, validator
import datetime
import utils.languages


class Url(BaseModel):
    """Schema for shortened URLs."""
    url: HttpUrl

    class Config:
        """Pydantic config section."""
        orm_mode = True
        schema_extra = {
            "example": {
                "url": "https://example.com"
            }
        }


class PasteBase(BaseModel):
    """Schema for pasted code."""
    language: str
    code: str

    class Config:
        """Pydantic config section."""
        schema_extra = {
            "example": {
                "language": "python",
                "code": "def add(a, b):\n    return a + b"
            }
        }

    @validator("language")
    def supported_language(cls, v: str) -> str:
        """Ensure the language of the paste is supported.

        Args:
            v (str): Value for the language field.

        Raises:
            ValueError: The value is not valid.

        Returns:
            str: The validated value.
        """
        v = v.lower().strip()
        if v not in utils.languages.language_ids:
            raise ValueError("Language not supported")
        return v


PasteCreate = PasteBase


class Paste(PasteBase):
    """Schema for pasted code."""
    hash: str

    class Config:
        """Pydantic config section."""
        orm_mode = True
        schema_extra = {
            "example": {
                "language": "python",
                "code": "def add(a, b):\n    return a + b",
                "hash": ("50d858e0985ecc7f60418aaf0cc5ab587f42c2570a884095a9e8"
                         "ccacd0f6545c")
            }
        }


class UploadBase(BaseModel):
    """Schema for uploaded files."""
    mimetype: str
    original_filename: str
    hash: str

    class Config:
        """Pydantic config section."""
        schema_extra = {
            "example": {
                "mimetype": "image/jpeg",
                "original_filename": "picture.jpeg",
                "hash": ("50d858e0985ecc7f60418aaf0cc5ab587f42c2570a884095a9e8"
                         "ccacd0f6545c")
            }
        }


class Upload(UploadBase):
    """Schema for uploaded files."""
    class Config:
        """Pydantic config section."""
        orm_mode = True


class UserBase(BaseModel):
    """Schema for users."""


class User(UserBase):
    """Schema for users."""


class ShortLink(BaseModel):
    """Schema for short links."""
    created: datetime.datetime
    updated: datetime.datetime
    url: Optional[Url]
    paste: Optional[Paste]
    upload: Optional[Upload]
    link: str
    expiry: Optional[datetime.datetime]

    class Config:
        """Pydantic config section."""
        orm_mode = True


class Token(BaseModel):
    """Schema for authentication tokens."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for authentication token data."""
    username: Optional[str] = None


class InstanceStats(BaseModel):
    """Schema for instance statistics."""
    shortened_links: int
    uploaded_files: int
    pasted_code: int
    total: int

    class Config:
        """Pydantic config section."""
        schema_extra = {
            "example": {
                "shortened_links": 3,
                "uploaded_files": 2,
                "pasted_code": 1,
                "total": 6
            }
        }


class InstanceInformation(BaseModel):
    """Schema for instance information."""
    url: str
    stats: InstanceStats
    admin: str
    version: str

    class Config:
        """Pydantic config section."""
        schema_extra = {
            "example": {
                "url": "https://quark.example",
                "admin": "Quark Admin <admin@quark.example>",
                "version": "1.0.0",
                "stats": {
                    "shortened_links": 3,
                    "uploaded_files": 2,
                    "pasted_code": 1,
                    "total": 6
                }
            }
        }
