from app.db import Base
from sqlalchemy import Column, String
from sqlalchemy.types import JSON


class Article(Base):
    __tablename__ = 'Article'

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
