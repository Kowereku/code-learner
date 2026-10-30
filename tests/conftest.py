from types import SimpleNamespace as NS

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.core.security import create_access_token
from src.main import app
from src.model.course import Course
from src.model.db import engine, get_db
from src.model.exercise import Exercise, ExerciseType
from src.model.lesson import Lesson
from src.model.module import Module
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


@pytest.fixture
def client(db):
    """An API client whose requests use the rolled-back session."""
    app.dependency_overrides[get_db] = lambda: db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.pop(get_db, None)


def auth_headers(user: User) -> dict[str, str]:
    """The header the frontend sends for a logged-in user."""
    return {"Authorization": f"Bearer {create_access_token({'sub': str(user.id)})}"}


@pytest.fixture
def course_tree(db):
    """A small Python course built for the test, so it doesn't depend on the seed data.

    A module with a lesson holding a code exercise, then a quiz module holding a chat question.
    """
    code = Exercise(
        type=ExerciseType.code,
        content="Print the numbers from 1 to 3 with a while loop.",
        code_snippet="i = 1\nwhile i <= 3:\n    print(i)\n    i += 1",
        correct_answer="1 2 3",
    )
    chat = Exercise(
        type=ExerciseType.chat,
        content="What is the difference between a list and a tuple?",
        correct_answer="A list can be changed, a tuple cannot.",
    )
    lesson = Lesson(
        title="Loops",
        xp_reward=10,
        exercises=[code],
        translations={"pl": {"title": "Pętle"}},
    )
    quiz = Lesson(title="Final quiz", xp_reward=20, is_quiz=True, exercises=[chat])
    course = Course(
        name="Test course",
        language="python",
        xp_reward=50,
        translations={"pl": {"name": "Kurs testowy"}},
        modules=[
            Module(title="Basics", order_index=1, lessons=[lesson]),
            Module(title="Quiz", order_index=2, lessons=[quiz]),
        ],
    )
    db.add(course)
    db.flush()
    return NS(course=course, lesson=lesson, quiz=quiz, code=code, chat=chat)
