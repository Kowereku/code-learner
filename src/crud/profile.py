from datetime import date

from sqlalchemy.orm import Session

from src.core.badges import closest_next
from src.core.profile import next_lesson, suggest_course
from src.crud import badge as badge_crud
from src.crud import course as course_crud
from src.crud import progress as progress_crud
from src.crud import user as user_crud
from src.model.user import User
from src.schemas.badge import BadgeRead
from src.schemas.course import CourseListItem
from src.schemas.profile import NextLessonRead, ProfileCourse, ProfileRead, ProfileStats


def _localized_title(item, locale: str) -> str:
    """Return the title in the requested language, falling back to the base one when missing or empty."""
    return ((item.translations or {}).get(locale) or {}).get("title") or item.title


def get_badges(db: Session, user: User, today: date) -> list[BadgeRead]:
    """Return all badges with progress. Read-only: badges are awarded when lessons are completed."""
    return badge_crud.list_badges(db, user, badge_crud.get_metrics(db, user, today))


def get_profile(db: Session, user: User, locale: str, today: date) -> ProfileRead:
    """Build the profile: stats, badges, started courses (in progress first) and a suggested course.

    Read-only: the streak shown is computed for today, nothing is written.
    """
    shown_user = user_crud.user_read(user, today)
    metrics = badge_crud.get_metrics(db, user, today)
    badges = badge_crud.list_badges(db, user, metrics)
    earned = [badge for badge in badges if badge.awarded_at]
    upcoming_badge = closest_next(metrics, {badge.code for badge in earned})

    courses = sorted(course_crud.get_courses(db), key=lambda course: course.id)
    completed_ids = {
        lesson_id for lesson_id, _ in progress_crud.get_completed_lessons(db, user.id)
    }

    in_progress: list[ProfileCourse] = []
    done: list[ProfileCourse] = []
    for course in courses:
        lesson_ids = {lesson.id for module in course.modules for lesson in module.lessons}
        completed_lessons = len(lesson_ids & completed_ids)
        if not completed_lessons:
            continue
        upcoming = next_lesson(course, completed_ids)
        item = ProfileCourse(
            course=CourseListItem.from_course(course, locale),
            completed_lessons=completed_lessons,
            completed=upcoming is None,
            next_lesson=(
                NextLessonRead(
                    id=upcoming[1].id,
                    title=_localized_title(upcoming[1], locale),
                    module_title=_localized_title(upcoming[0], locale),
                )
                if upcoming
                else None
            ),
        )
        (done if upcoming is None else in_progress).append(item)

    started_ids = {item.course.id for item in in_progress + done}
    suggested = suggest_course(courses, started_ids, user.track)

    return ProfileRead(
        user=shown_user,
        stats=ProfileStats(
            total_xp=user.total_xp,
            streak_days=shown_user.streak_days,
            courses_completed=len(done),
            badges_earned=len(earned),
        ),
        latest_badge=max(earned, key=lambda badge: badge.awarded_at, default=None),
        next_badge=next(
            (badge for badge in badges if upcoming_badge and badge.code == upcoming_badge.code),
            None,
        ),
        courses=in_progress + done,
        suggested_course=CourseListItem.from_course(suggested, locale) if suggested else None,
    )
