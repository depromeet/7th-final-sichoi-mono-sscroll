from app.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Integer


class Log(Base):

    __tablename__ = 'log'

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='logs')

    article_id = Column(Integer, ForeignKey('article.id'))
    article = relationship('Article', back_populates='logs')
