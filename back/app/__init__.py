# flake8: noqa
# isort:skip_file
from flask import Flask

from app import db
from app.config import Config
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
CORS(app, supports_credentials=True)


from app.api import *
