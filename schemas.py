"""Pydantic schemas."""
from typing import Optional
from pydantic import BaseModel, HttpUrl, EmailStr
import datetime


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
    expires: datetime.date

    class Config:
        """Pydantic config section."""
        schema_extra = {
            "example": {
                "mimetype": "image/jpeg",
                "original_filename": "picture.jpeg",
                "hash": ("50d858e0985ecc7f60418aaf0cc5ab587f42c2570a884095a9e8"
                         "ccacd0f6545c"),
                "expires": "2020-01-01"
            }
        }


class Upload(UploadBase):
    """Schema for uploaded files."""
    class Config:
        """Pydantic config section."""
        orm_mode = True


class UserBase(BaseModel):
    """Schema for users."""
    name: Optional[str]
    email: EmailStr

    class Config:
        """Pydantic config section."""
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "hi@example.com"
            }
        }


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    name: Optional[str]
    email: Optional[EmailStr]

    class Config:
        """Pydantic config section."""
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "hi@example.com"
            }
        }


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str

    class Config:
        """Pydantic config section."""
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "hi@example.com",
                "password": "password123"
            }
        }


class User(UserBase):
    """Schema for users."""
    created: datetime.date
    updated: datetime.date
    confirmed: bool
    confirmed_on: Optional[datetime.date]

    class Config:
        """Pydantic config section."""
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1337,
                "name": "John Doe",
                "created": "2020-01-01",
                "updated": "2020-01-01",
                "email": "hi@example.com",
                "confirmed": True,
                "confirmed_on": "2020-01-01"
            }
        }


class ShortLink(BaseModel):
    """Schema for short links."""
    created: datetime.date
    updated: datetime.date
    url: Optional[Url]
    paste: Optional[Paste]
    upload: Optional[Upload]
    link: str

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
                "url": "https://example.vh7.uk",
                "admin": "Example Admin <hi@example.vh7.uk>",
                "version": "1.0.0",
                "stats": {
                    "shortened_links": 3,
                    "uploaded_files": 2,
                    "pasted_code": 1,
                    "total": 6
                }
            }
        }
