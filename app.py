from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from sqlalchemy import MetaData
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URL") or "sqlite:///" + os.path.join(
        basedir, "app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


app = Flask(__name__)
app.config.from_object(Config)

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# from models import models
from routes import routes
