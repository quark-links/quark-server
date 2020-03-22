"""A file containing the configuration for the VH7 instance.

All of these values should be set through environment variables, but they can
be manually edited here if they need to be.
"""

import os
from distutils.dist import Distribution

dist = Distribution()
dist.parse_config_files()
VERSION = dist.get_option_dict("bumpversion")["current_version"][1]

# URI for creating a database connection with SQLAlchemy. Defaults to a local
# SQLite database.
SQLALCHEMY_DATABASE_URI = os.getenv("VH7_DB_CONNECTION_STRING",
                                    "sqlite:///db.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Recycle connections after 5 minutes
SQLALCHEMY_POOL_RECYCLE = 300

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
UPLOAD_MIN_AGE = int(os.getenv("VH7_UPLOAD_MIN_AGE", 30))
# The maximum age that an uploaded file is stored for in days.
UPLOAD_MAX_AGE = int(os.getenv("VH7_UPLOAD_MAX_AGE", 90))
# The maximum size that uploaded files are allowed to be in Mb.
UPLOAD_MAX_SIZE = int(os.getenv("VH7_UPLOAD_MAX_SIZE", 256))

# The maximum file size that the server will accept before aborting the
# request.
MAX_CONTENT_LENGTH = UPLOAD_MAX_SIZE * 1024 * 1024


INSTANCE_NAME = os.getenv("VH7_INSTANCE_NAME", "Unnamed VH7 Instance")
INSTANCE_URL = os.getenv("VH7_INSTANCE_URL", "https://example.com/")
INSTANCE_EMAIL = os.getenv("VH7_INSTANCE_EMAIL", "hi@example.com")
INSTANCE_COUNTRY = os.getenv("VH7_INSTANCE_COUNTRY", "United Kingdom")
