from .BaseSync import BaseSync  # noqa
from ...utils import safe_get


class UserSync(BaseSync):  # noqa

    @staticmethod
    def mongo_to_pg(session, mongo_entry, user):
        """Replicate a MongoDB document to a SQLAlchemy mapped instance."""
        _id = str(mongo_entry.get('_id'))
        assert _id

        # transfer the fields over
        user._id = _id
        user.name = safe_get(mongo_entry, 'name')
