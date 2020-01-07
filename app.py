"""The main entrypoint for VH7.

This file is the entrypoint for running VH7. It starts up Flask and sets up the
database.
"""

from flask import Flask, render_template
from db import db
from flask_cors import CORS
from api.routes import api
import os

# Create a new Flask server
app = Flask(__name__)
# Load configuration from the 'config.py' file
app.config.from_object("config")

# Setup CORS on the Flask application
CORS(app)

# Setup the SQLAlchemy database
db.init_app(app)
db.app = app
# Create all of the tables in the database
db.create_all()
# Save changes
db.session.commit()

# Create the upload folder if it doesn't exist
try:
    os.makedirs(app.config["UPLOAD_FOLDER"])
except FileExistsError:
    pass

# Load API routes
app.register_blueprint(api)


@app.route("/")
def index():
    """The main index page."""
    return render_template("home.jinja2")


if __name__ == '__main__':
    app.run()
