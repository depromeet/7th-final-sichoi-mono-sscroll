from app.db import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import String


class User(Base):

    __tablename__ = 'user'

    key = Column(UUID, unique=True)
    logs: 'Log' = relationship('Log', back_populates='user')
