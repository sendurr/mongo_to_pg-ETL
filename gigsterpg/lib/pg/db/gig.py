from sqlalchemy import (  # noqa
    Column,
    ForeignKey,
    INTEGER,
    TIMESTAMP,
    VARCHAR
)
from sqlalchemy.orm import relationship

from ._base import Base, EnumType


class Gig(Base):  # noqa
    __tablename__ = 'gigs'

    id = Column(INTEGER, primary_key=True)

    # Information about the job request
    _id = Column(VARCHAR(64), unique=True)
    created = Column(TIMESTAMP)
    updated = Column(TIMESTAMP)

    GIG_STATE = [
        'cancelled',
        'done',
        'in_progress',
        'unstarted',
    ]
    state = Column(
        EnumType(GIG_STATE),
        nullable=False)
