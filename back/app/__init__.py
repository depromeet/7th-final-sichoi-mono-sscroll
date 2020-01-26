# flake8: noqa
# isort:skip_file
from flask import Flask
from flask_session import Session

from app import db
from app.config import Config
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True)
session = Session(app)


from app.api import *
