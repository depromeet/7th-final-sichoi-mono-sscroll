import json
import random
from typing import Any

from app import app, models
from app.context import ApiContext
from app.decorators import router
from app.models.article import Article
from app.models.log import Log
from flask import session
from sqlalchemy.sql.expression import func

route: Any = router(app)


@route('/', methods=['GET'])
def index(context: ApiContext) -> dict:
    return {'sscroll': 'hi'}


@route('/content', methods=['GET'])
def get_content(context: ApiContext) -> list:
    articles = (
        context.query(Article)
        .filter(~Article.logs.any(Log.user == context.user))
        .order_by(func.random())
        .limit(2)
        .all()
    )
    return [article.to_json() for article in articles]


@route('/content/<int:id>/read', methods=['POST'])
def read_content(context: ApiContext, id) -> dict:
    article = context.query(Article).get(id)
    log = Log(user=context.user, article=article)
    context.session.add(log)
    return article.to_json()
