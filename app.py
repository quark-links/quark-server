from flask import Flask
from db import db
from flask_cors import CORS
import os
from api.routes import api


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("VH7_DB_CONNECTION_STRING",
                                                  "sqlite:///db.sqlite")
app.config["UPLOAD_FOLDER"] = os.getenv("VH7_UPLOAD_FOLDER", os.path.join(
                              os.path.dirname(os.path.realpath(__file__)),
                              "uploads/"))
CORS(app)
app.secret_key = "keyboardcat"
db.init_app(app)
db.app = app
db.create_all()
db.session.commit()

app.register_blueprint(api)


if __name__ == '__main__':
    app.run()
