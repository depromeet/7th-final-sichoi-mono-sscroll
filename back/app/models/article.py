from sqlalchemy import Column, String
from sqlalchemy.types import JSON

from app.db import Base


class Article(Base):
    __tablename__ = 'article'

    title = Column(String)
    body = Column(String)
    source = Column(String)

    def to_json(self):
        return {
            'title': self.title,
            'body': self.body,
            'source': self.source,
            'id': self.id,
        }
