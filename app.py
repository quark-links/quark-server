from flask import Flask, request
from flask_marshmallow import Marshmallow
from db import db, ShortLink, LongUrl
from flask_cors import CORS
import os
from api.request_schema import CreateShortLinkSchema
from url_normalize import url_normalize
from api.routes import api


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_CONNECTION_STRING", "sqlite:///db.sqlite")
CORS(app)
app.secret_key = "keyboardcat"
db.init_app(app)
db.app = app
db.create_all()
db.session.commit()

app.register_blueprint(api)

"""
@app.route("/")
def test():
    url = "https://google.co.uk/"
    longurl = LongUrl(url)
    shortlink = ShortLink("test")
    longurl.shortlink = shortlink

    db.session.add(shortlink)
    db.session.add(longurl)
    db.session.commit()
    return "ok"

    #shortlinks = ShortLink.query.all()
    #return shortlinks_schema.jsonify(shortlinks)
"""

if __name__ == '__main__':
    app.run()
