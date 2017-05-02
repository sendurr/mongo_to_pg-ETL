"""Library for database access."""
from collections import OrderedDict
import os

import alembic.config
from path import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from ._base import Base
from .gig import Gig
from .skill import Skill
from .user import User
# from .user_skill import UserSkill # uncomment when the join table is in place
from gigsterpg.lib.utils import PATH_TO_ALEMBIC_INI

# NOTE: order matters! some entities have non-nullable foreign keys (e.g.
#   milestones require gig_ids)
ALL_TABLES = OrderedDict([
    # hardcoded enums
    ('skill', Skill),
    ('user', User),
    # ('user_skill', UserSkill), # uncomment when the join table in place
    ('gig', Gig),
])

for module_name, table_class in ALL_TABLES.items():
    def defrepr(cls):  # noqa
        if hasattr(cls, '_id'):
            identifier = cls._id
        elif hasattr(cls, 'id'):
            identifier = cls.id
        else:
            identifier = ''

        return '<%s %s>' % (cls.__class__.__name__, identifier)

    if not hasattr(table_class, '__repr__'):
        table_class.__repr__ = defrepr

    def as_dict(cls):  # noqa
        return {c.name: getattr(cls, c.name) for c in cls.__table__.columns}
    table_class.as_dict = as_dict


class SqlAlchemy(object):
    """This class is used to manage the SQLAlchemy database connection."""

    def __init__(self):
        """Create a engine and (thread-local) session factory.

        The connecting string is read from the environment variable
        `DB_URL_PSQL`.
        """
        self.engine = create_engine(
            os.environ['DB_URL_PSQL'],
            pool_size=5,
            pool_recycle=3600,
            echo=False,
            # http://docs.sqlalchemy.org/en/rel_1_0/dialects/mysql.html#mysql-isolation-level
            isolation_level='READ COMMITTED',
        )
        self.Base = Base
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def migrate_head(self):
        """Migrate to the latest schema."""
        with Path(PATH_TO_ALEMBIC_INI):
            alembic.config.main(argv=[
                '--raiseerr',
                'upgrade', 'head',
            ])

    def migrate_base(self):
        """Migrate to an empty schema."""
        with Path(PATH_TO_ALEMBIC_INI):
            alembic.config.main(argv=[
                '--raiseerr',
                'downgrade', 'base',
            ])

    @property
    def has_existing_tables(self):
        """Return True if non-public (standard) tables exist in the database."""
        existing_table_count = self.engine \
            .execute("""SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'\
                AND table_name<>'alembic_version';""") \
            .scalar()
        return existing_table_count > 0
