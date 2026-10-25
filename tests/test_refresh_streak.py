from datetime import date, timedelta

from sqlalchemy.orm import Session

from src.crud.user import refresh_streak
from src.model.db import engine
from src.model.user import User


def test_refresh_streak_resets_a_broken_streak():
    """Runs against the dev database inside a transaction that is rolled back."""
    with engine.connect() as conn:
        tx = conn.begin()
        db = Session(bind=conn, join_transaction_mode="create_savepoint")
        user = User(
            username="streak_probe",
            email="streak_probe@example.com",
            password="x",
            streak_days=4,
            last_activity_date=date.today() - timedelta(days=3),
        )
        db.add(user)
        db.flush()
        assert refresh_streak(db, user).streak_days == 0
        db.close()
        tx.rollback()
