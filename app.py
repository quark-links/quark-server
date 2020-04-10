"""The main entrypoint for VH7.

This file is the entrypoint for running VH7. It starts up Flask and sets up the
database.
"""

from flask import Flask, render_template, redirect, send_file, request
from flask import Response
from flask_migrate import Migrate
from db import db, hashids, ShortLink, User
from flask_cors import CORS
from api.routes import api
from users.routes import user_blueprint
import os
import config
import cleanup
import utils.languages as lang
from flask_login import LoginManager
from flask_mail import Mail
import users.api_keys as api_keys
from api.exceptions import AuthenticationException

# Create a new Flask server
app = Flask(__name__)
# Load configuration from the 'config.py' file
app.config.from_object("config")

# Setup CORS on the Flask application
CORS(app)

# Setup the SQLAlchemy database
db.init_app(app)
db.app = app

migrate = Migrate(app, db)

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"
login_manager.refresh_view = "users.login"
login_manager.needs_refresh_message = ("To protect your account, we require "
                                       "that you reauthenticate before "
                                       "accessing this page.")
login_manager.needs_refresh_message_category = "warning"

# Setup mail
mail = Mail()
mail.init_app(app)

# Create the upload folder if it doesn't exist
try:
    os.makedirs(app.config["UPLOAD_FOLDER"])
except FileExistsError:
    pass

# Load API routes
app.register_blueprint(api)
app.register_blueprint(user_blueprint)


@login_manager.user_loader
def load_user(id):
    """Find a user in the database by their id."""
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def load_user_from_request(request):
    """Find a user in the database by their API key."""
    if request.blueprint == "api":
        api_key = request.headers.get("Authorization")
        if api_key:
            api_key = api_key.replace("Bearer ", "", 1)
            user = api_keys.verify_api_key(api_key)

            if user is None:
                raise AuthenticationException()
            else:
                return user

    return None


@app.route("/")
def index():
    """The main index page."""
    return render_template("home.jinja2", languages=lang.languages)


@app.route("/privacy")
def privacy():
    """The privacy policy page."""
    return render_template("privacy.jinja2")


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
        language = lang.get_language_by_id(shortlink.paste.language)

        if request.args.get("dl") is not None:
            return Response(shortlink.paste.code, headers={
                "Content-disposition":
                    "attachment; filename=paste-{}{}".format(
                        shortlink.link(False), language["filetype"])
            })
        else:
            return render_template("paste.jinja2",
                                   paste=shortlink.paste,
                                   language=language)
    elif shortlink.upload is not None:
        if (request.args.get("dl") is not None and
                shortlink.upload.filename is not None):
            # Get the path of the upload by joining the filename with the
            # upload directory
            path = os.path.join(config.UPLOAD_FOLDER,
                                shortlink.upload.filename)
            filename = shortlink.upload.original_filename

            return send_file(path, as_attachment=True,
                             attachment_filename=filename,
                             mimetype=shortlink.upload.mimetype)
        else:
            return render_template("download.jinja2", upload=shortlink.upload)
    else:
        raise Exception("Short Link isn't pointed to any other type!")


cleanup.start()

if __name__ == '__main__':
    app.run()
