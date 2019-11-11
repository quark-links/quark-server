from flask import Flask, render_template
from db import db
from flask_cors import CORS
from api.routes import api
import os


app = Flask(__name__)
app.config.from_object("config")
CORS(app)
db.init_app(app)
db.app = app
db.create_all()
db.session.commit()

try:
    os.makedirs(app.config["UPLOAD_FOLDER"])
except FileExistsError:
    pass

app.register_blueprint(api)


@app.route("/")
def index():
    return render_template("home.jinja2")


if __name__ == '__main__':
    app.run()
