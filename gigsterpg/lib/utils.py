"""Various utility functions."""
import os
import re

from gigsterpg import __path__ as package_path

PATH_TO_ALEMBIC_INI = os.path.dirname(package_path[0])  # there is one entry


def clean_unicodeing(unicodeing):
    """Clean a unicodeing."""
    if not unicodeing:
        return unicodeing

    unicodeing = re.sub("(\u2018|\u2019|\u201c|\u201d)", "'", unicodeing)
    unicodeing = re.sub("(\u2013)", "-", unicodeing)

    return unicodeing


def safe_get(dictionary, field):
    """Safe version of Get."""
    x = dictionary.get(field)

    if isinstance(x, str):
        return clean_unicodeing(x)

    return x


def upsert_field(field, obj, session, value):
    """Update or insert an instance in the obj table given a field.

    If the field already exists in the obj table, then associate
    that field with that user/gig. Else, create one and then associate.

    Args:
        field: (str) a field (attribute) belonging to
    the obj table (mapped class)
        obj: (Object) a sqlalchemy mapped class
        sessoin: a sqlachemy session
        value: the value to be inserted or queried
    Return:
        An obj Object
    """
    instance = session.query(obj).filter(getattr(obj, field) == value).all()
    if len(instance) > 0:
        # update
        return session.query(obj).filter(getattr(obj, field) == value).one()
    else:
        # insert
        temp = obj()
        setattr(temp, field, value)
        return temp
