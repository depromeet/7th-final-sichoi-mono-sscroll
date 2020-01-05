from typing import Any, Union

from flask import session as mem_session
from sqlalchemy.orm import Query, Session
from werkzeug.wrappers import Request

from app.models import Base


class ApiContext:

    session: Session
    request: Request
    data: dict = {}

    def __init__(self, session: Session, request: Request):
        self.session = session
        self.request = request

        if self.request.method == 'POST':
            self.data = self.request.json
        elif self.request.method == 'GET':
            self.data = self.request.args

    def query(self, model: Base) -> Query:
        return self.session.query(model)
