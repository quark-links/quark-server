from flask import Flask
from db import db
from flask_cors import CORS
from api.routes import api


app = Flask(__name__)
app.config.from_object("config")
CORS(app)
db.init_app(app)
db.app = app
db.create_all()
db.session.commit()

app.register_blueprint(api)


if __name__ == '__main__':
    app.run()
