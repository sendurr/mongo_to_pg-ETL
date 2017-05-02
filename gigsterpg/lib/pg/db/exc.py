# noqa
class Error(Exception):
    """Base class for exceptions in this module."""


class InvalidEmailException(Error):
    """Exception raised for invalid email addresses."""

    def __init__(self, email):  # noqa
        Error.__init__(self)
        self.email = email


class EnumOOBException(Error):
    """Exception raised for an EnumType taking an invalid value."""

    def __init__(self, value, allow_values):  # noqa
        Error.__init__(self)
        self.value = value
        self.allow_values = allow_values
