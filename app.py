"""The main entrypoint for VH7.

This file is the entrypoint for running VH7. It starts up Flask and sets up the
database.
"""

from flask import Flask, render_template, redirect, send_file
from db import db, hashids, ShortLink
from flask_cors import CORS
from api.routes import api
import os
import config

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


@app.route("/<id>")
def goto(id):
    """Route for managing redirects from a short link."""
    try:
        id = hashids.decode(id)[0]
    except IndexError:
        return ("Sorry! That short link is invalid, please ensure that you "
                "have typed it correctly.")

    # Lookup the short link from the id
    shortlink = ShortLink.query.filter_by(id=id).first()

    if shortlink.url is not None:
        # Redirect user to the URL
        return redirect(shortlink.url.url, 301)
    elif shortlink.paste is not None:
        return shortlink.paste.code
    elif shortlink.upload is not None:
        # Get the path of the upload by joining the filename with the upload
        # directory
        path = os.path.join(config.UPLOAD_FOLDER, shortlink.upload.filename)
        filename = shortlink.upload.original_filename

        return send_file(path, as_attachment=True,
                         attachment_filename=filename,
                         mimetype=shortlink.upload.mimetype)
    else:
        raise Exception("Short Link isn't pointed to any other type!")


if __name__ == '__main__':
    app.run()
