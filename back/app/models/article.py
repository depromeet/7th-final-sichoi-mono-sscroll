from app.db import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON


class Article(Base):
    __tablename__ = 'article'

    title = Column(String)
    body = Column(String)
    source = Column(String)
    logs = relationship('Log', back_populates='article')

    def to_json(self):
        return {
            'title': self.title,
            'body': self.body,
            'source': self.source,
            'id': self.id,
        }
