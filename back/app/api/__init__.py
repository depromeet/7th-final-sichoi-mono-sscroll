import json
import random
from typing import Any, Iterable, List

from flask import session
from sqlalchemy import desc
from sqlalchemy.sql.expression import func

from app import app
from app.context import ApiContext
from app.decorators import router
from app.models.article import Article
from app.models.log import Log

route = router(app)


@app.route('/', methods=['GET'])
def index() -> dict:
    return {'sscroll': 'hi'}


@route('/content', methods=['GET'])
def get_contents(context: ApiContext) -> list:

    articles: List[Article] = []
    pop_count = 2
    if 'created' in session:
        articles += (
            context.query(Article)
            .join(Article.logs)
            .filter(Article.source != 'humoruniv')
            .group_by(Article.id, Log.article_id)
            .order_by(desc(func.count(Article.logs)))
            .limit(30)
            .all()
        )
        del session['created']
        pop_count = 10
    else:
        articles += (
            context.query(Article)
            .filter(Article.source != 'humoruniv')
            .filter(~Article.logs.any(Log.user == context.user))
            .order_by(func.random())
            .limit(20)
            .all()
        )
    random.shuffle(articles)
    articles = [articles.pop() for i in range(pop_count)]
    return [article.to_json() for article in articles]


@route('/content/<int:id>', methods=['GET'])
def get_content(context: ApiContext, id) -> dict:
    article: Article = context.query(Article).get(id)
    return article.to_json()


@route('/content/<int:id>/read', methods=['POST'])
def read_content(context: ApiContext, id) -> dict:
    article = context.query(Article).get(id)
    log = Log(user=context.user, article=article)
    context.session.add(log)
    return article.to_json()
