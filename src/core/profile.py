"""Pure helpers for the profile page: the next lesson to take and the course to suggest."""


def next_lesson(course, completed_ids: set[int]):
    """Return (module, lesson) for the first lesson not completed yet, or None when all are done.

    Modules are walked by order_index and lessons by id, the order the course page shows them in.
    """
    for module in sorted(course.modules, key=lambda m: m.order_index):
        for lesson in sorted(module.lessons, key=lambda l: l.id):
            if lesson.id not in completed_ids:
                return module, lesson
    return None


def suggest_course(courses, started_ids: set[int], track: str | None):
    """Return the first not-started course from the user's area, else any not-started course."""
    fresh = [course for course in courses if course.id not in started_ids]
    in_area = (course for course in fresh if track and course.track == track)
    return next(in_area, None) or next(iter(fresh), None)
