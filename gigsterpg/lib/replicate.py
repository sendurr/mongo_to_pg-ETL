"""Database library to replicate the database from MongoDB to Postgres."""
from datetime import datetime, timedelta as td

import pymongo
from tqdm import tqdm

from .db_mongo import gigster_db
from .pg import sync
from .pg.db.gig import Gig
from .pg.db.user import User


def identity_tqdm_func(record, total):
    """an identity tqdm function"""
    return record


class Replicator(object):
    """This class is used to replicate documents from MongoDB to Postgres tables."""

    # MongoDB collection name, ORM class, sync module, max number to replicate
    # (None<=>replicate all),
    COLLECTION_TABLE_MAPPING = [
        ('users', User, sync.UserSync),
        ('gigs', Gig, sync.GigSync),
    ]

    def __init__(
            self,
            db,
            collections=None,
            force=False,
            limit=None,
            logger=None,
            use_tqdm=False):
        """
        Create an instance of a replicator.

        :param db:              SqlAlqhemy DB connection
        :param collections:     MongoDB collections to replicate.  Default value of None
                                is interpreted to mean to process all collection types.
        :param force:           Force tables to update regardless of whether or not they
                                have been replicated recently.  This defaults to False.
        :param limit:           Maximium number of documents to replicate for a
                                given collection type.  This defaults None.
        :param logger:          A logger Object. Default is None.
        """
        self.db = db
        self.collections = collections
        self.force = force
        self.limit = limit
        self.logger = logger

        self._loop_decorator_func = identity_tqdm_func
        if use_tqdm:
            self._loop_decorator_func = tqdm

    def replicate(self):
        """Synchronize all document / tables."""
        self.db.session.autoflush = False

        # assume all collections are allowed if no collections are specified
        if self.collections is None:
            self.collections = [c[0] for c in Replicator.COLLECTION_TABLE_MAPPING]

        for mongo_name, mapped_class, sync_module in Replicator.COLLECTION_TABLE_MAPPING:
            if mongo_name not in self.collections:
                if self.logger:
                    self.logger.info('Skipping collection {}'.format(mongo_name))
                continue
            self.replicate_table(
                mongo_name, mapped_class, sync_module,
                limit=self.limit, force=self.force)

    def cache_sql_table(self, mapped_class, key_attribute='_id'):
        """
        Caches all instances of a SQLAlchemy mapped class currently in the SQL
        database in an in-memory dict, using `key_attribute` for the dictionary
        keys.
        """
        results = self.db.session.query(mapped_class).all()
        all_sql_entries = {}
        for r in results:
            all_sql_entries[getattr(r, key_attribute)] = r
        return all_sql_entries

    def replicate_table(
            self,
            mongo_name,
            mapped_class,
            sync_module,
            ids=None,
            limit=None,
            force=False):
        """
        Replicate the entries from a MongoDB Collection to a Postgres table.

        If `ids` is specified, only MongoDB documents with matching `_id`s will be replicated.
        """
        if self.logger:
            self.logger.info('Replicating Table {} => {}'.format(mongo_name, mapped_class.__tablename__))

        mongo_collection = getattr(gigster_db, mongo_name)

        if ids:
            # limit the entries to the ones requested
            objectIds = [{'$oid': o} for o in ids]
            query = {
                '_id': {
                    '$in': [
                        objectIds
                    ]
                }
            }
            all_mongo_entries = mongo_collection.find(query)

        else:
            # query all mongoDB entries
            all_mongo_entries = mongo_collection.find(
                {},
                no_cursor_timeout=True
            ).sort('$natural', pymongo.DESCENDING)

        if limit:
            all_mongo_entries.limit(limit)

        successes = 0
        failures = 0

        all_sql_entries = self.cache_sql_table(mapped_class)
        for mongo_entry in self._loop_decorator_func(
                all_mongo_entries, total=all_mongo_entries.count()):

            _id = str(mongo_entry['_id'])

            # create a pg record, or update the existing one
            sql_entry = all_sql_entries.get(_id)
            recently_replicated = None
            if sql_entry:
                recently_replicated = (
                    datetime.now() - sql_entry.created) < td(hours=1)

            # skip over the sql entry

            if sql_entry and recently_replicated and not force:
                if self.logger:
                    self.logger.debug('SKIPPING ENTRY %s\t%s' %
                                      (mapped_class.__tablename__, _id))
                continue

            else:

                if sql_entry:
                    if self.logger:
                        self.logger.debug('UPDATING ENTRY %s\t%s' %
                                          (mapped_class.__tablename__, _id))
                else:
                    if self.logger:
                        self.logger.debug('CREATING ENTRY %s\t%s' %
                                          (mapped_class.__tablename__, _id))
                    sql_entry = mapped_class()
                    self.db.session.add(sql_entry)

            # map the mongoDB properties to pg record
            try:
                sync_module.mongo_to_pg(self.db.session, mongo_entry, sql_entry)
                self.db.session.commit()
                successes += 1
            except Exception:
                if self.logger:
                    self.logger.exception({'mongo_entry': {'_id': _id}})
                self.db.session.rollback()
                failures += 1

        if self.logger:
            self.logger.info('Finished Table {}'.format(mongo_name))
            self.logger.info('\tsuccesses {}'.format(successes))
            self.logger.info('\tfailures {}'.format(failures))
