import pytest  # noqa

from gigsterpg.lib.pg import db as _db


@pytest.fixture(scope='session')
def db():
    """Session-wide test database."""
    db = _db.SqlAlchemy()
    if db.has_existing_tables:
        db.migrate_base()
    db.migrate_head()

    return db


@pytest.fixture(scope='function')
def session(db):
    """Create a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    yield db.session()
    # truncate all the tables except from the skills tables
    for table in reversed(db.Base.metadata.sorted_tables):
        if table.name != 'skills':
            connection.execute(table.delete())

    transaction.commit()

    db.session.close()
    connection.close()
