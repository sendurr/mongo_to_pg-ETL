import os  # noqa

from alembic import context
from gigsterpg.lib.pg.db import skill
from gigsterpg.lib.pg.db._base import Base
from gigsterpg.logger import json_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

logger = json_logger()

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a connection string
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    standard output (STDOUT).

    """
    url = os.environ['DB_URL_PSQL']
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(
        os.environ['DB_URL_PSQL'],
        pool_size=5,
        pool_recycle=3600,
        echo=False,
        # http://docs.sqlalchemy.org/en/rel_1_0/dialects/mysql.html#mysql-isolation-level
        isolation_level='READ COMMITTED',
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

        # if we are upgrading, set up the event listeners, else, don't, because
        # a downgrade migration will remove the tables and raise errors when the
        # tables aren't there for listeners.
        if context.config.cmd_opts.cmd[0].__name__ == 'upgrade':      # 0: the first argument after `alembic` in
            session = scoped_session(sessionmaker(bind=connectable))  # `alembic downgrade base`, i.e. the downgrade

            if len(session.query(skill.Skill).all()) == 0:  # only populate if empty
                skill.populate(session)

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
