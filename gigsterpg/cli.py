"""Main entry point for the cron job to replicate all documents from the MongDB Gigster main database to Postgres."""
import argparse
import os

from gigsterpg.lib.pg import db as _db
from gigsterpg.lib.replicate import Replicator
from gigsterpg.logger import json_logger

db = _db.SqlAlchemy()
db.migrate_head()

env = os.environ.get('ENV')
default_boolean = False
if env and env.upper() in ['DEV', 'DEVELOPMENT']:
    default_boolean = True


# Initialize parser
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--limit', default=-1, type=int,
                    help='Limit the number of entries replicated per collection')
parser.add_argument('--force', default=False, action='store_true',
                    help='Force replication even if recently replicated')
parser.add_argument('--list_tables', default=None,
                    help='List the current tables')
parser.add_argument('--use_tqdm', default=default_boolean, action='store_true',
                    help='Use tqdm for clear output')
parser.add_argument('--collections', default=None,
                    help='Limit the replication to only the collections specified (comma separated)')
parser.add_argument('--loglevel', default='INFO',
                    help='Level of logging to use (default: WARNING, values: CRITICAL, ERROR, WARNING, INFO, DEBUG)')
args = parser.parse_args()


if __name__ == "__main__":
    collections = None
    if args.collections:
        collections = args.collections.split(',')

    limit = args.limit if args.limit > -1 else None

    logger = json_logger(level=args.loglevel)

    try:
        logger.info('Running in environment: {}'.format(os.environ['ENV']))
    except Exception:
        logger.exception('Error: environment not initialized')
        exit()

    kwargs = {
        'limit': limit,
        'force': args.force,
        'collections': collections,
        'logger': logger,
        'use_tqdm': args.use_tqdm
    }

    replicator = Replicator(db, **kwargs)
    replicator.replicate()
