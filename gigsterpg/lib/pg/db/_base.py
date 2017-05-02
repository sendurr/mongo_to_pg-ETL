"""
Creates the declarative base which all of the models import.

Contains code for custom SqlAlchemy Database types and modifiers.
"""

from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.types as types
import validators

from .exc import (
    EnumOOBException,
    InvalidEmailException,
)


# Declarative base for building models
Base = declarative_base()


# SQLAlchemy Custom Data Types
##########################################################################

class EnumType(types.TypeDecorator):
    """Python based enumeration."""

    impl = types.VARCHAR(32)

    def __init__(self, allow_values):  # noqa
        self.allow_values = allow_values
        super(EnumType, self).__init__()

    def process_bind_param(self, value, dialect):
        """Saving to DB."""
        if not value:
            return value
        if value not in self.allow_values:
            raise EnumOOBException(value=value, allow_values=self.allow_values)
        return value

    def process_result_value(self, value, dialect):
        """Retrieve value from database."""
        # assert not value or value in self.allow_values
        return value


class EmailType(types.TypeDecorator):
    """A field which represents an email address."""

    impl = types.VARCHAR(128)

    def __init__(self):  # noqa
        super(EmailType, self).__init__()

    def process_bind_param(self, value, dialect):
        """Saving an email field to the database."""
        if not value or not value.strip():
            return None

        if value.startswith('mailto:'):
            value = value[len('mailto:'):]

        email_valid = validators.email(value)
        if not email_valid:
            raise InvalidEmailException(email=value)

        # email values are always lower case
        value = value.lower()
        return value

    def process_result_value(self, value, dialect):
        """Retrieve value from database."""
        return value
