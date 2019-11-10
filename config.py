import os

SQLALCHEMY_DATABASE_URI = os.getenv("VH7_DB_CONNECTION_STRING",
                                    "sqlite:///db.sqlite")
UPLOAD_FOLDER = os.getenv("VH7_UPLOAD_FOLDER", os.path.join(os.path.dirname(
                          os.path.realpath(__file__)), "uploads/"))
SECRET_KEY = os.getenv("VH7_SECRET", "keyboardcat")
HASHIDS_ALPHABET = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234"
                    "56789")
HASHIDS_SALT = os.getenv("VH7_SALT", "keyboardcat")
