from typing import Optional
from pydantic import BaseModel, HttpUrl, EmailStr, validator
import datetime
from urllib.parse import urljoin
from os import getenv
import utils.idencode


class Url(BaseModel):
    url: HttpUrl

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "url": "https://example.com"
            }
        }


class PasteBase(BaseModel):
    language: str
    code: str

    class Config:
        schema_extra = {
            "example": {
                "language": "python",
                "code": "def add(a, b):\n    return a + b"
            }
        }


PasteCreate = PasteBase


class Paste(PasteBase):
    hash: str

    class Config:
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
    mimetype: str
    original_filename: str
    hash: str
    expires: datetime.date

    class Config:
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
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: Optional[str]
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "hi@example.com"
            }
        }


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "hi@example.com"
            }
        }


class UserCreate(UserBase):
    password: str

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "hi@example.com",
                "password": "password123"
            }
        }


class User(UserBase):
    created: datetime.date
    updated: datetime.date
    confirmed: bool
    confirmed_on: Optional[datetime.date]

    class Config:
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
    id: int
    created: datetime.date
    updated: datetime.date
    url: Optional[Url]
    paste: Optional[Paste]
    upload: Optional[Upload]
    # user: Optional[User]
    link: str = None

    @validator("link", pre=True, always=True)
    def default_link(cls, v, *, values, **kwargs):
        link = urljoin(getenv("INSTANCE_URL", "https://vh7.uk/"),
                       utils.idencode.encode(values['id']))
        return v or link

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class InstanceStats(BaseModel):
    shortened_links: int
    uploaded_files: int
    pasted_code: int
    total: int

    class Config:
        schema_extra = {
            "example": {
                "shortened_links": 3,
                "uploaded_files": 2,
                "pasted_code": 1,
                "total": 6
            }
        }


class InstanceInformation(BaseModel):
    url: str
    stats: InstanceStats
    admin: str
    version: str

    class Config:
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
