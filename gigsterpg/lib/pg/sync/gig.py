from .BaseSync import BaseSync  # noqa
from ...utils import safe_get



class GigSync(BaseSync):  # noqa

    @staticmethod
    def mongo_to_pg(session, mongo_entry, gig):
        """Replicate a MongoDB document to a Postgres table."""
        _id = str(mongo_entry.get('_id'))
        assert _id

        #   transfer the fields over
        ##########################################
        gig._id = _id

        gig.description = safe_get(mongo_entry, 'description')

        session.flush()
