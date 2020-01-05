from sqlalchemy import Column
from sqlalchemy.types import JSON

from app.db import Base
from app.models.article import Article


class Packet(Base):
    __tablename__ = "Packet"

    request_header = Column(JSON)
    request_body = Column(JSON)

    response_header = Column(JSON)
    response_body = Column(JSON)
