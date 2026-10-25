from sqlalchemy.orm import Session

from src.crud.badge import sync_badges
from src.model.db import engine
from src.model.user import User


def test_sync_is_idempotent():
    """Runs against the dev database inside a transaction that is rolled back."""
    with engine.connect() as conn:
        tx = conn.begin()
        db = Session(bind=conn)
        user = User(
            username="sync_probe", email="sync_probe@example.com", password="x", best_streak=3
        )
        db.add(user)
        db.flush()
        assert [b.code for b in sync_badges(db, user)] == ["streak_3"]
        assert sync_badges(db, user) == []
        db.close()
        tx.rollback()
