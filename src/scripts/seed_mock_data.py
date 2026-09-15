"""Database mock data seeding script for code-learner.

Seeds initial courses, modules, lessons, and exercises into the database
if the courses table is empty (or when run with --force).

Run via:
    uv run python -m src.scripts.seed_mock_data
or
    .venv/Scripts/python.exe src/scripts/seed_mock_data.py
"""

from __future__ import annotations

import logging
import sys

from src.model.course import Course
from src.model.db import SessionLocal
from src.model.exercise import Exercise
from src.model.lesson import Lesson
from src.model.module import Module

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def seed_mock_data(force: bool = False) -> None:
    """Populate initial mock courses, modules, lessons, and exercises."""
    db = SessionLocal()
    try:
        course_count = db.query(Course).count()
        if course_count > 0 and not force:
            logger.info(
                "Table 'courses' already contains %s records. Skipping mock data seeding. "
                "Use --force to overwrite.",
                course_count,
            )
            return

        if force and course_count > 0:
            logger.info("Force flag detected. Clearing existing courses...")
            db.query(Course).delete()
            db.commit()

        logger.info("Seeding mock courses data...")

        # Course 1: Web Development
        course_1 = Course(
            name="Web Development",
            icon_url="🌐",
            description=(
                "Build interactive websites, modern user interfaces, and dynamic "
                "web applications from scratch."
            ),
        )

        # Course 2: Data Science & AI
        course_2 = Course(
            name="Data Science & AI",
            icon_url="📊",
            description=(
                "Analyze complex data, train machine learning models, and explore "
                "artificial intelligence using Python."
            ),
        )

        # Course 3: Backend Engineering
        course_3 = Course(
            name="Backend Engineering",
            icon_url="⚙️",
            description=(
                "Design the invisible logic, manage databases, and build scalable "
                "server architectures that power the web."
            ),
        )

        # Course 4: Cybersecurity & Linux
        course_4 = Course(
            name="Cybersecurity & Linux",
            icon_url="🛡️",
            description=(
                "Master the command line, identify system vulnerabilities, and learn "
                "the fundamentals of secure network infrastructure."
            ),
        )

        # Cascade under "Data Science & AI": Module -> Lesson -> Exercises
        module_ds = Module(
            title="Python Basics",
            order_index=1,
        )
        course_2.modules.append(module_ds)

        lesson_ds = Lesson(
            title="Your First Script",
            xp_reward=15,
        )
        module_ds.lessons.append(lesson_ds)

        ex_1 = Exercise(
            type="block_assembly",
            content="Ułóż bloczki kodu w odpowiedniej kolejności, aby wyświetlić powitanie 'Hello, World!'.",
            code_snippet="print('Hello, World!')",
            correct_answer="print('Hello, World!')",
        )
        ex_2 = Exercise(
            type="multiple_choice",
            content="Która z poniższych funkcji w języku Python służy do wypisywania tekstu na ekranie?",
            code_snippet=None,
            correct_answer="print()",
        )
        ex_3 = Exercise(
            type="matching",
            content="Dopasuj operatory w języku Python do ich przeznaczenia: '+' -> dodawanie, '*' -> mnożenie, '**' -> potęgowanie.",
            code_snippet=None,
            correct_answer="+: dodawanie; *: mnożenie; **: potęgowanie",
        )
        lesson_ds.exercises.extend([ex_1, ex_2, ex_3])

        db.add_all([course_1, course_2, course_3, course_4])
        db.commit()

        logger.info(
            "Database successfully seeded with 4 courses! Course 'Data Science & AI' (ID: %s) "
            "has module '%s' (ID: %s), lesson '%s' (ID: %s), and %s exercises.",
            course_2.id,
            module_ds.title,
            module_ds.id,
            lesson_ds.title,
            lesson_ds.id,
            len(lesson_ds.exercises),
        )
    except Exception:
        db.rollback()
        logger.exception("Error occurred while seeding mock data.")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    force_flag = "--force" in sys.argv
    seed_mock_data(force=force_flag)
