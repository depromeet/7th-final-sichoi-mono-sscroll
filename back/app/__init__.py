# flake8: noqa
# isort:skip_file
from flask import Flask

from app import db
from app.config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


from app.api import *
