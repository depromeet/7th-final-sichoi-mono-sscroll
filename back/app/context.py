from typing import Any, Union
from uuid import uuid4

from app.models import Base, User
from flask import session as mem_session
from sqlalchemy.orm import Query, Session
from werkzeug.wrappers import Request


class ApiContext:

    session: Session
    request: Request
    user: User
    data: dict = {}

    def __init__(self, session: Session, request: Request):
        self.session = session
        self.request = request

        if 'id' not in mem_session:
            key = str(uuid4())
            self.session.add(User(key=key))
            self.session.flush()
            mem_session['id'] = key

        key = mem_session['id']
        self.user = self.query(User).filter(User.key == key).first()
        if not self.user:
            self.user = User(key=key)
            self.session.add(self.user)
            self.session.flush()

        if self.request.method == 'POST':
            self.data = self.request.json
        elif self.request.method == 'GET':
            self.data = self.request.args

    def query(self, model: Base) -> Query:
        return self.session.query(model)
