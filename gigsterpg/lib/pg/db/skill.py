from sqlalchemy import Column, INTEGER, VARCHAR  # noqa

from ._base import Base
from .enumerations import SKILLS


class Skill(Base):  # noqa

    __tablename__ = "skills"

    id = Column(INTEGER, primary_key=True)

    name = Column(VARCHAR(64), unique=True, nullable=False)

    def __init__(self, name):  # noqa
        self.name = name


def populate(dbSession):  # noqa
    """The initial entries which should be placed into this database."""
    for s in SKILLS:
        skill = Skill(name=s)
        dbSession.add(skill)
    dbSession.commit()
