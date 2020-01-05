import json
import random
from typing import Any

from app import app, models
from app.context import ApiContext
from app.decorators import router
from app.models.article import Article
from flask import session
from sqlalchemy.sql.expression import func

route: Any = router(app)


@route('/', methods=['GET'])
def index(context: ApiContext):
    return {'sscroll': 'hi'}


@route('/content', methods=['GET'])
def get_content(context: ApiContext):
    article = (
        context.session.query(Article).order_by(func.random()).limit(1).first()
    )
    return article.to_json()
