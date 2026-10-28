from datetime import date, datetime, timezone

from src.crud.badge import award_badges, get_metrics, sync_badges
from src.crud.leaderboard import rank_of
from src.crud.progress import complete_lesson
from src.model.course import Course
from src.model.exercise import Exercise, ExerciseType
from src.model.lesson import Lesson
from src.model.module import Module
from src.model.user_lesson import UserLesson

TODAY = date(2026, 10, 25)


def test_sync_is_idempotent(db, make_user):
    user = make_user(best_streak=3)
    assert [b.code for b in sync_badges(db, user, TODAY)] == ["streak_3"]
    assert sync_badges(db, user, TODAY) == []


def test_award_skips_badges_inserted_meanwhile(db, make_user):
    # Two completions racing: the second insert of the same badge must not fail.
    user = make_user()
    now = datetime.now(timezone.utc)
    assert award_badges(db, user.id, ["streak_3"], now) == ["streak_3"]
    assert award_badges(db, user.id, ["streak_3"], now) == []


def test_each_code_exercise_counts_once_even_on_replays(db, make_user):
    user = make_user()
    lesson = (
        db.query(Lesson)
        .join(Exercise, Exercise.lesson_id == Lesson.id)
        .filter(Exercise.type == ExerciseType.code)
        .first()
    )
    code_ids = [e.id for e in lesson.exercises if e.type == ExerciseType.code]
    other_id = next(e.id for e in db.query(Exercise) if e.lesson_id != lesson.id)
    complete_lesson(db, user, lesson, 0, TODAY, code_ids + [other_id])
    complete_lesson(db, user, lesson, 0, TODAY, code_ids)
    assert get_metrics(db, user, TODAY).code_answers == len(code_ids)


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
    assert get_metrics(db, user, TODAY).courses_completed == 1


def _first_lesson(db) -> Lesson:
    """The first lesson of the first course: not a quiz, and finishing it doesn't finish the course."""
    course = db.query(Course).order_by(Course.id).first()
    module = min(course.modules, key=lambda m: m.order_index)
    lesson = min(module.lessons, key=lambda lesson: lesson.id)
    # The level tests below rely on this: fail clearly if the seed data ever changes.
    assert not lesson.is_quiz and lesson.xp_reward >= 5
    return lesson


def test_crossing_a_level_reports_it(db, make_user):
    user = make_user(total_xp=295)
    result = complete_lesson(db, user, _first_lesson(db), 0, TODAY)
    assert (result.level_before, result.level_after) == (2, 3)
    assert result.rank == rank_of(db, result.total_xp)
    assert "level_3" in [b.code for b in result.new_badges]


def test_replay_keeps_level(db, make_user):
    user = make_user(total_xp=295)
    lesson = _first_lesson(db)
    complete_lesson(db, user, lesson, 0, TODAY)
    replay = complete_lesson(db, user, lesson, 0, TODAY)
    assert replay.level_before == replay.level_after == 3
