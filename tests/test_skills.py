from datetime import datetime, timedelta # noqa

import pytest  # noqa
from gigsterpg.lib.pg.db.skill import Skill
from gigsterpg.lib.pg.db.user import User
from gigsterpg.lib.pg.db.user_skill import UserSkill
from gigsterpg.lib.pg.sync.user import UserSync


@pytest.fixture(scope='function')
def setup_session(session):
    """Prepare the conftest.session for every function in this module and yield."""
    user_objects = [
        {
            "_id": 0,  # NOTE: this is placeholder the mongo id and NOT the primary key id
            "name": "Plump Plumber",
            "email": "pp@yggdrasil.com",
            "skills": ['Engineer, agricultural', 'Chief Financial Officer']
        },
        {
            "_id": 1,
            "name": "Plump lumber",
            "email": "pl@yggdrasil.com",
            "skills": ['Ranger/warden', 'Therapist, horticultural']
        },
    ]

    for user_object in user_objects:
        user_instance = User()
        UserSync.mongo_to_pg(
            session,
            user_object,
            user_instance
        )

        session.add(user_instance)

    session.commit()

    yield session


def test_tables_should_only_have_the_two_records_fixtured(setup_session):  # noqa
    assert len(setup_session.query(UserSkill).all()) == 4
    assert len(setup_session.query(Skill).all()) > 0


def test_user_skills_should_be_replicated(setup_session):  # noqa
    assert len(setup_session.query(UserSkill).all()) > 0
    #  0th index to get the first entry in users.
    #  Get the skills object for user_0
    skills_set_of_user_0 = {user_skill.skill.name: 0 for user_skill in
                            setup_session.query(User).filter(User._id == '0').one().skills}
    # The replicated the skills should be the declared
    for skill in ['Engineer, agricultural', 'Chief Financial Officer']:
        skills_set_of_user_0[skill] += 1

    assert sum(skills_set_of_user_0.values()) == 2


def test_duplicate_user_skills_should_resolve_to_same_entry(setup_session):  # noqa
    # A `set` is being called on the list of skills to clean out potential redundancies.
    # a `set` hashes so it does not preserve the ordering of the skills. This test
    # makes sure that if two skills of two users have the same name then they are the
    # same skill objects.
    skills_set_of_user_0 = [user_skill.skill for user_skill in
                            setup_session.query(User).filter(User._id == '0').one().skills]
    skills_set_of_user_1 = [user_skill.skill for user_skill in
                            setup_session.query(User).filter(User._id == '1').one().skills]
    for skill_of_user_0 in skills_set_of_user_0:
        for skill_of_user_1 in skills_set_of_user_1:
            if skill_of_user_0.name == skill_of_user_1.name:
                assert skill_of_user_0 is skill_of_user_1
