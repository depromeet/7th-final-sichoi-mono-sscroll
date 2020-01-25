from app.db import Base
from app.models.article import Article
from app.models.log import Log
from app.models.user import User
from sqlalchemy import Column
from sqlalchemy.types import JSON


class Packet(Base):
    __tablename__ = "packet"

    request_header = Column(JSON)
    request_body = Column(JSON)

    response_header = Column(JSON)
    response_body = Column(JSON)
