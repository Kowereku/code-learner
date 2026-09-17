"""Database seeding script for code-learner.

Populates the database with an initial course, module, lessons, and Dual Mode coding exercises.
Run via:
    uv run python -m src.scripts.seed
or
    make seed
"""

from src.model.course import Course
from src.model.db import SessionLocal
from src.model.exercise import Exercise, ExerciseType
from src.model.lesson import Lesson
from src.model.module import Module


def seed_database() -> None:
    db = SessionLocal()
    try:
        existing_course = db.query(Course).filter(Course.name == "Podstawy Pythona").first()
        if existing_course:
            print(f"Course 'Podstawy Pythona' already exists (ID: {existing_course.id}). Skipping seed.")
            return

        print("Seeding initial course: 'Podstawy Pythona'...")
        course = Course(
            name="Podstawy Pythona",
            description=(
                "Rozpocznij naukę programowania od zera! Ucz się w trybie Dual Mode: "
                "łącząc intuicyjne bloczki z prawdziwym kodem w edytorze tekstowym."
            ),
            icon_url="https://raw.githubusercontent.com/github/explore/main/topics/python/python.png",
        )
        db.add(course)
        db.flush()

        # Module 1: Pierwsze kroki w Pythonie
        module_1 = Module(
            course_id=course.id,
            title="Pierwsze kroki w Pythonie",
            order_index=1,
        )
        db.add(module_1)
        db.flush()

        # Lesson 1: Funkcja print i zmienne
        lesson_1 = Lesson(
            module_id=module_1.id,
            title="Wypisywanie tekstu i zmienne",
            xp_reward=10,
        )
        db.add(lesson_1)
        db.flush()

        ex_1 = Exercise(
            lesson_id=lesson_1.id,
            type=ExerciseType.code,
            content="Napisz program, który wypisze w konsoli powitanie 'Witaj świecie!'.",
            code_snippet='print("Witaj świecie!")',
            correct_answer="Witaj świecie!",
        )
        ex_2 = Exercise(
            lesson_id=lesson_1.id,
            type=ExerciseType.code,
            content="Stwórz zmienną imie o wartości 'Jan' i wypisz ją za pomocą funkcji print.",
            code_snippet='imie = "Jan"\nprint(imie)',
            correct_answer="Jan",
        )
        db.add_all([ex_1, ex_2])

        # Lesson 2: Instrukcje warunkowe
        lesson_2 = Lesson(
            module_id=module_1.id,
            title="Instrukcje warunkowe if / else",
            xp_reward=15,
        )
        db.add(lesson_2)
        db.flush()

        ex_3 = Exercise(
            lesson_id=lesson_2.id,
            type=ExerciseType.code,
            content=(
                "Sprawdź czy zmienna punkty jest większa lub równa 50. "
                "Jeśli tak, wypisz 'Zdane', w przeciwnym wypadku 'Poprawka'."
            ),
            code_snippet='punkty = 75\nif punkty >= 50:\n    print("Zdane")\nelse:\n    print("Poprawka")',
            correct_answer="Zdane",
        )
        db.add(ex_3)

        db.commit()
        print(
            f"Database successfully seeded! Created Course (ID: {course.id}) with 1 modules, 2 lessons, and 3 exercises."
        )
    except Exception as e:
        db.rollback()
        print(f"Error occurred while seeding the database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
