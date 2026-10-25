from datetime import datetime, timezone

from src.crud.badge import award_badges, get_metrics, sync_badges
from src.crud.progress import complete_lesson
from src.model.course import Course
from src.model.exercise import Exercise, ExerciseType
from src.model.lesson import Lesson
from src.model.module import Module
from src.model.user_lesson import UserLesson


def test_sync_is_idempotent(db, make_user):
    user = make_user(best_streak=3)
    assert [b.code for b in sync_badges(db, user)] == ["streak_3"]
    assert sync_badges(db, user) == []


def test_award_skips_badges_inserted_meanwhile(db, make_user):
    # Two requests racing: the second insert of the same badge must not fail.
    user = make_user()
    now = datetime.now(timezone.utc)
    assert award_badges(db, user.id, ["streak_3"], now) == ["streak_3"]
    assert award_badges(db, user.id, ["streak_3"], now) == []


def test_code_answers_are_capped_at_the_lessons_code_exercises(db, make_user):
    user = make_user()
    lesson = (
        db.query(Lesson)
        .join(Exercise, Exercise.lesson_id == Lesson.id)
        .filter(Exercise.type == ExerciseType.code)
        .first()
    )
    code_count = sum(1 for e in lesson.exercises if e.type == ExerciseType.code)
    complete_lesson(db, user, lesson, mistakes_made=0, code_answers=99)
    assert user.code_answers == code_count


def test_courses_completed_counts_courses_with_every_lesson_done(db, make_user):
    # No user_courses row, as for accounts that finished a course before auto-completion existed.
    user = make_user()
    course = db.query(Course).order_by(Course.id).first()
    lesson_ids = (
        db.query(Lesson.id).join(Module, Module.id == Lesson.module_id).filter(Module.course_id == course.id)
    )
    now = datetime.now(timezone.utc)
    db.add_all(
        UserLesson(user_id=user.id, lesson_id=lesson_id, completed_at=now, status="completed")
        for (lesson_id,) in lesson_ids
    )
    db.flush()
    assert get_metrics(db, user).courses_completed == 1
