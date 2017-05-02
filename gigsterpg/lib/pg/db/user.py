from sqlalchemy import (  # noqa
    Column,
    INTEGER,
    TIMESTAMP,
    VARCHAR,
)
from sqlalchemy.orm import relationship

from ._base import Base, EmailType


class User(Base):  # noqa
    __tablename__ = 'users'
    id = Column(INTEGER, primary_key=True)
    _id = Column(VARCHAR(64), unique=True)
    created = Column(TIMESTAMP)
    updated = Column(TIMESTAMP)

    email = Column(EmailType(), nullable=True, unique=True)

    name = Column(VARCHAR(64), nullable=False)
