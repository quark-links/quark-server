"""A file containing the configuration for the VH7 instance.

All of these values should be set through environment variables, but they can
be manually edited here if they need to be.
"""

import os

# URI for creating a database connection with SQLAlchemy. Defaults to a local
# SQLite database.
SQLALCHEMY_DATABASE_URI = os.getenv("VH7_DB_CONNECTION_STRING",
                                    "sqlite:///db.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# The folder where uploaded files should go. Defaults to 'uploads' in the base
# of the project.
UPLOAD_FOLDER = os.getenv("VH7_UPLOAD_FOLDER", os.path.join(os.path.dirname(
                          os.path.realpath(__file__)), "uploads/"))

# A secret key for encrypting Flask cookies.
SECRET_KEY = os.getenv("VH7_SECRET", "keyboardcat")

# The alphabet that short links can be made from. Use only URL-safe characters
# and do not change after initial run!
HASHIDS_ALPHABET = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234"
                    "56789")

# The salt that short links are generated from. Do not change after initial
# run!
HASHIDS_SALT = os.getenv("VH7_SALT", "keyboardcat")

# The minimum age that an uploaded file is stored for in days.
UPLOAD_MIN_AGE = 30
# The maximum age that an uploaded file is stored for in days.
UPLOAD_MAX_AGE = 90
# The maximum size that uploaded files are allowed to be in Mb.
UPLOAD_MAX_SIZE = 256

# The maximum file size that the server will accept before aborting the
# request.
MAX_CONTENT_LENGTH = UPLOAD_MAX_SIZE * 1024 * 1024
