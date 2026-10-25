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
from src.schemas.user import UserRead


def _localized_title(item, locale: str) -> str:
    """Return the title in the requested language, falling back to the base one."""
    return ((item.translations or {}).get(locale) or {}).get("title", item.title)


def _refresh(db: Session, user: User) -> None:
    """Bring the streak and badges up to date before reading them."""
    user_crud.refresh_streak(db, user)
    badge_crud.sync_badges(db, user)
    db.commit()


def get_badges(db: Session, user: User) -> list[BadgeRead]:
    """Return all badges with progress, after awarding any the user already qualifies for."""
    _refresh(db, user)
    return badge_crud.list_badges(db, user)


def get_profile(db: Session, user: User, locale: str) -> ProfileRead:
    """Build the profile: stats, badges, started courses (in progress first) and a suggested course."""
    badges = get_badges(db, user)
    earned = [badge for badge in badges if badge.awarded_at]
    upcoming_badge = closest_next(
        badge_crud.get_metrics(db, user), {badge.code for badge in earned}
    )

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
        user=UserRead.model_validate(user),
        stats=ProfileStats(
            total_xp=user.total_xp,
            streak_days=user.streak_days,
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
