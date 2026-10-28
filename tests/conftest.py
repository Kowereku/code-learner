import pytest
from sqlalchemy.orm import Session

from src.model.db import engine
from src.model.user import User


@pytest.fixture
def db():
    """A session on the dev database whose changes are rolled back after the test.

    Commits inside the code under test only release a savepoint, so nothing is kept.
    """
    with engine.connect() as conn:
        tx = conn.begin()
        session = Session(bind=conn, join_transaction_mode="create_savepoint")
        try:
            yield session
        finally:
            session.close()
            tx.rollback()


@pytest.fixture
def make_user(db):
    """Create a throwaway user inside the rolled-back session."""

    def make(**fields) -> User:
        defaults = dict(username="probe", email="probe@example.com", password="x")
        user = User(**(defaults | fields))
        db.add(user)
        db.flush()
        return user

    return make
