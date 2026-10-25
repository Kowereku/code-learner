"""Database seeding script for code-learner.

Populates the database with initial courses, modules, lessons, and Dual Mode coding exercises.
Run via:
    uv run python -m src.scripts.seed
or
    make seed
"""

import sys

from src.model.course import Course, Track
from src.model.db import SessionLocal
from src.model.exercise import Exercise, ExerciseType
from src.model.lesson import Lesson
from src.model.module import Module
from src.scripts.seed_tracks import seed_track_courses


def seed_database(force: bool = False) -> None:
    db = SessionLocal()
    try:
        existing_courses = (
            db.query(Course)
            .filter(Course.name.in_(["Python Basics", "React Fundamentals"]))
            .all()
        )
        if existing_courses and not force:
            existing_names = ", ".join(f"'{c.name}'" for c in existing_courses)
            print(
                f"Courses already exist in database ({existing_names}). Skipping seed. "
                "Use --force to overwrite."
            )
            seed_track_courses(db)
            return

        if force:
            print("Force flag detected. Removing existing seed courses...")
            to_remove = (
                db.query(Course)
                .filter(
                    Course.name.in_(
                        [
                            "Python Basics",
                            "React Fundamentals",
                            "Podstawy Pythona",
                            "React od podstaw",
                        ]
                    )
                )
                .all()
            )
            for c in to_remove:
                db.delete(c)
            db.commit()
        else:
            # Clean up legacy Polish course versions if present
            legacy_courses = (
                db.query(Course)
                .filter(Course.name.in_(["Podstawy Pythona", "React od podstaw"]))
                .all()
            )
            if legacy_courses:
                for c in legacy_courses:
                    db.delete(c)
                db.commit()

        # =========================================================================
        # Course 1: Python Basics
        # =========================================================================
        print("Seeding initial course: 'Python Basics'...")
        course_python = Course(
            name="Python Basics",
            description=(
                "Start programming from scratch! Learn in Dual Mode: "
                "combining intuitive visual blocks with real code in a text editor."
            ),
            icon_url="https://raw.githubusercontent.com/github/explore/main/topics/python/python.png",
            language="python",
            track=Track.data_science,
            xp_reward=150,
            translations={
                "pl": {
                    "name": "Podstawy Pythona",
                    "description": (
                        "Zacznij programować od zera! Ucz się w trybie Dual Mode: łącząc "
                        "intuicyjne bloki wizualne z prawdziwym kodem w edytorze tekstu."
                    ),
                }
            },
        )
        db.add(course_python)
        db.flush()

        # -------------------------------------------------------------------------
        # Course 1 / Module 1: First Steps in Python
        # -------------------------------------------------------------------------
        module_py_1 = Module(
            course_id=course_python.id,
            title="First Steps in Python",
            translations={"pl": {"title": "Pierwsze kroki w Pythonie"}},
            order_index=1,
        )
        db.add(module_py_1)
        db.flush()

        # Lesson 1.1: Printing text and variables
        lesson_py_1_1 = Lesson(
            module_id=module_py_1.id,
            title="Printing Text and Variables",
            translations={"pl": {"title": "Wypisywanie tekstu i zmienne"}},
            xp_reward=10,
        )
        db.add(lesson_py_1_1)
        db.flush()

        ex_py_10 = Exercise(
            lesson_id=lesson_py_1_1.id,
            type=ExerciseType.block_assembly,
            content='Display the text "Hello Polycode" on the screen.',
            translations={"pl": {"content": 'Wyświetl na ekranie tekst "Hello Polycode".'}},
            correct_answer='print ( "Hello Polycode" )',
            options=["print", "(", '"Hello Polycode"', ")", ";", "cout", "[", "]", "echo"],
        )
        db.add(ex_py_10)

        ex_py_1 = Exercise(
            lesson_id=lesson_py_1_1.id,
            type=ExerciseType.code,
            content='Write a program that prints "Hello, World!" to the console.',
            translations={"pl": {"content": 'Napisz program, który wypisze w konsoli "Hello, World!".'}},
            code_snippet='print("Hello, World!")',
            correct_answer="Hello, World!",
        )
        ex_py_2 = Exercise(
            lesson_id=lesson_py_1_1.id,
            type=ExerciseType.code,
            content='Create a variable named name with the value "John" and print it using the print function.',
            translations={
                "pl": {"content": 'Utwórz zmienną name o wartości "John" i wypisz ją za pomocą funkcji print.'}
            },
            code_snippet='name = "John"\nprint(name)',
            correct_answer="John",
        )
        db.add_all([ex_py_1, ex_py_2])

        ex_py_18 = Exercise(
            lesson_id=lesson_py_1_1.id,
            type=ExerciseType.multiple_choice,
            content="Which function displays text on the screen in Python?",
            translations={"pl": {"content": "Która funkcja wyświetla tekst na ekranie w Pythonie?"}},
            correct_answer="print()",
            options=["print()", "echo()", "console.log()"],
        )
        ex_py_19 = Exercise(
            lesson_id=lesson_py_1_1.id,
            type=ExerciseType.multiple_choice,
            content='Which line stores the text "Duck" in a variable named pet?',
            translations={"pl": {"content": 'Która linia zapisuje tekst "Duck" w zmiennej o nazwie pet?'}},
            correct_answer='pet = "Duck"',
            options=['pet = "Duck"', '"Duck" = pet', 'pet == "Duck"'],
        )
        db.add_all([ex_py_18, ex_py_19])

        # Lesson 1.2: Conditional statements
        lesson_py_1_2 = Lesson(
            module_id=module_py_1.id,
            title="Conditional Statements (if / else)",
            translations={"pl": {"title": "Instrukcje warunkowe (if / else)"}},
            xp_reward=15,
        )
        db.add(lesson_py_1_2)
        db.flush()

        ex_py_11 = Exercise(
            lesson_id=lesson_py_1_2.id,
            type=ExerciseType.multiple_choice,
            content="Which keyword runs code when the if condition is false?",
            translations={"pl": {"content": "Które słowo kluczowe uruchamia kod, gdy warunek if jest fałszywy?"}},
            correct_answer="else",
            options=["else", "otherwise", "then"],
        )
        db.add(ex_py_11)

        ex_py_3 = Exercise(
            lesson_id=lesson_py_1_2.id,
            type=ExerciseType.code,
            content=(
                "Create a variable 'score' with the value 75. If score is greater than or "
                "equal to 50, print 'Pass', otherwise print 'Retake'."
            ),
            translations={
                "pl": {
                    "content": (
                        "Utwórz zmienną 'score' o wartości 75. Jeśli score jest większy lub równy 50, "
                        "wypisz 'Pass', w przeciwnym razie wypisz 'Retake'."
                    )
                }
            },
            code_snippet='score = 75\nif score >= 50:\n    print("Pass")\nelse:\n    print("Retake")',
            correct_answer="Pass",
        )
        db.add(ex_py_3)

        # Lesson 1.3: While loops and basic operations
        lesson_py_1_3 = Lesson(
            module_id=module_py_1.id,
            title="While Loops and Logical Operators",
            translations={"pl": {"title": "Pętle while i operatory logiczne"}},
            xp_reward=15,
        )
        db.add(lesson_py_1_3)
        db.flush()

        ex_py_12 = Exercise(
            lesson_id=lesson_py_1_3.id,
            type=ExerciseType.multiple_choice,
            content="Which operator means 'and' in Python?",
            translations={"pl": {"content": "Który operator oznacza 'i' (and) w Pythonie?"}},
            correct_answer="and",
            options=["and", "&&", "&"],
        )
        db.add(ex_py_12)

        ex_py_4 = Exercise(
            lesson_id=lesson_py_1_3.id,
            type=ExerciseType.code,
            content="Write a while loop that prints numbers from 1 to 3.",
            translations={"pl": {"content": "Napisz pętlę while, która wypisze liczby od 1 do 3."}},
            code_snippet='i = 1\nwhile i <= 3:\n    print(i)\n    i += 1',
            correct_answer="1\n2\n3",
        )
        db.add(ex_py_4)

        # -------------------------------------------------------------------------
        # Course 1 / Module 2: Data Structures in Python
        # -------------------------------------------------------------------------
        module_py_2 = Module(
            course_id=course_python.id,
            title="Data Structures in Python",
            translations={"pl": {"title": "Struktury danych w Pythonie"}},
            order_index=2,
        )
        db.add(module_py_2)
        db.flush()

        # Lesson 2.1: Lists and indexing
        lesson_py_2_1 = Lesson(
            module_id=module_py_2.id,
            title="Lists and Indexing Elements",
            translations={"pl": {"title": "Listy i indeksowanie elementów"}},
            xp_reward=20,
        )
        db.add(lesson_py_2_1)
        db.flush()

        ex_py_13 = Exercise(
            lesson_id=lesson_py_2_1.id,
            type=ExerciseType.multiple_choice,
            content="Which represents an empty list in Python?",
            translations={"pl": {"content": "Co oznacza pustą listę w Pythonie?"}},
            correct_answer="[ ]",
            options=["[ ]", "( )", "{ }"],
        )
        db.add(ex_py_13)

        ex_py_5 = Exercise(
            lesson_id=lesson_py_2_1.id,
            type=ExerciseType.code,
            content="Create a list named 'fruits' containing 'apple' and 'banana', then print its first element.",
            translations={
                "pl": {
                    "content": "Utwórz listę o nazwie 'fruits' zawierającą 'apple' i 'banana', a następnie wypisz jej pierwszy element."
                }
            },
            code_snippet='fruits = ["apple", "banana"]\nprint(fruits[0])',
            correct_answer="apple",
        )
        db.add(ex_py_5)

        # Lesson 2.2: For loop and iteration
        lesson_py_2_2 = Lesson(
            module_id=module_py_2.id,
            title="For Loops and Iteration",
            translations={"pl": {"title": "Pętle for i iteracja"}},
            xp_reward=20,
        )
        db.add(lesson_py_2_2)
        db.flush()

        ex_py_14 = Exercise(
            lesson_id=lesson_py_2_2.id,
            type=ExerciseType.block_assembly,
            content="Build a loop that goes over every number in the list numbers.",
            translations={"pl": {"content": "Zbuduj pętlę, która przejdzie po każdej liczbie z listy numbers."}},
            correct_answer="for number in numbers :",
            options=["for", "number", "in", "numbers", ":", "each", "of", ";"],
        )
        db.add(ex_py_14)

        ex_py_6 = Exercise(
            lesson_id=lesson_py_2_2.id,
            type=ExerciseType.code,
            content="Create a list named 'numbers' with the values 1, 2 and 3, then use a for loop to print every number from it.",
            translations={
                "pl": {
                    "content": "Utwórz listę o nazwie 'numbers' z wartościami 1, 2 i 3, a następnie użyj pętli for, aby wypisać każdą liczbę."
                }
            },
            code_snippet='numbers = [1, 2, 3]\nfor number in numbers:\n    print(number)',
            correct_answer="1\n2\n3",
        )
        db.add(ex_py_6)

        # Lesson 2.3: Dictionaries and key-value pairs
        lesson_py_2_3 = Lesson(
            module_id=module_py_2.id,
            title="Dictionaries and Key-Value Pairs",
            translations={"pl": {"title": "Słowniki i pary klucz-wartość"}},
            xp_reward=25,
        )
        db.add(lesson_py_2_3)
        db.flush()

        ex_py_15 = Exercise(
            lesson_id=lesson_py_2_3.id,
            type=ExerciseType.matching,
            content="Select the matching pairs.",
            translations={
                "pl": {
                    "content": "Dopasuj pary.",
                    "correct_answer": 'Lista: [1, 2, 3]; Krotka: ("a", "b"); Słownik: {"id": 1}; Liczba: 67; Napis: "Duck"',
                    "options": [
                        ["Lista", "[1, 2, 3]"],
                        ["Krotka", '("a", "b")'],
                        ["Słownik", '{"id": 1}'],
                        ["Liczba", "67"],
                        ["Napis", '"Duck"'],
                    ],
                }
            },
            correct_answer='List: [1, 2, 3]; Tuple: ("a", "b"); Dictionary: {"id": 1}; Number: 67; String: "Duck"',
            options=[
                ["List", "[1, 2, 3]"],
                ["Tuple", '("a", "b")'],
                ["Dictionary", '{"id": 1}'],
                ["Number", "67"],
                ["String", '"Duck"'],
            ],
        )
        db.add(ex_py_15)

        ex_py_7 = Exercise(
            lesson_id=lesson_py_2_3.id,
            type=ExerciseType.code,
            content="Create a dictionary named 'person' with key 'name' set to 'Anna', and print the value of this key.",
            translations={
                "pl": {
                    "content": "Utwórz słownik o nazwie 'person' z kluczem 'name' ustawionym na 'Anna' i wypisz wartość tego klucza."
                }
            },
            code_snippet='person = {"name": "Anna"}\nprint(person["name"])',
            correct_answer="Anna",
        )
        db.add(ex_py_7)

        # -------------------------------------------------------------------------
        # Course 1 / Module 3: Functions and Modularity
        # -------------------------------------------------------------------------
        module_py_3 = Module(
            course_id=course_python.id,
            title="Functions and Modularity",
            translations={"pl": {"title": "Funkcje i modularność"}},
            order_index=3,
        )
        db.add(module_py_3)
        db.flush()

        # Lesson 3.1: Defining custom functions
        lesson_py_3_1 = Lesson(
            module_id=module_py_3.id,
            title="Defining Functions (def)",
            translations={"pl": {"title": "Definiowanie funkcji (def)"}},
            xp_reward=25,
        )
        db.add(lesson_py_3_1)
        db.flush()

        ex_py_16 = Exercise(
            lesson_id=lesson_py_3_1.id,
            type=ExerciseType.block_assembly,
            content="Start the definition of a function named greet.",
            translations={"pl": {"content": "Rozpocznij definicję funkcji o nazwie greet."}},
            correct_answer="def greet ( ) :",
            options=["def", "greet", "(", ")", ":", "function", "{", "fn"],
        )
        db.add(ex_py_16)

        ex_py_8 = Exercise(
            lesson_id=lesson_py_3_1.id,
            type=ExerciseType.code,
            content="Define a function named 'greet()' that prints 'Hello!'. Call this function.",
            translations={"pl": {"content": "Zdefiniuj funkcję 'greet()', która wypisze 'Hello!'. Wywołaj tę funkcję."}},
            code_snippet='def greet():\n    print("Hello!")\n\ngreet()',
            correct_answer="Hello!",
        )
        db.add(ex_py_8)

        # Lesson 3.2: Parameters and return values
        lesson_py_3_2 = Lesson(
            module_id=module_py_3.id,
            title="Parameters and Return Values (return)",
            translations={"pl": {"title": "Parametry i zwracanie wartości (return)"}},
            xp_reward=30,
        )
        db.add(lesson_py_3_2)
        db.flush()

        ex_py_17 = Exercise(
            lesson_id=lesson_py_3_2.id,
            type=ExerciseType.multiple_choice,
            content="Which keyword sends a value back from a function?",
            translations={"pl": {"content": "Które słowo kluczowe zwraca wartość z funkcji?"}},
            correct_answer="return",
            options=["return", "print", "send"],
        )
        db.add(ex_py_17)

        ex_py_9 = Exercise(
            lesson_id=lesson_py_3_2.id,
            type=ExerciseType.code,
            content="Write a function 'add(a, b)' that returns the sum of two numbers. Print the result of add(2, 3).",
            translations={
                "pl": {"content": "Napisz funkcję 'add(a, b)', która zwraca sumę dwóch liczb. Wypisz wynik add(2, 3)."}
            },
            code_snippet='def add(a, b):\n    return a + b\n\nprint(add(2, 3))',
            correct_answer="5",
        )
        db.add(ex_py_9)

        module_py_quiz = Module(
            course_id=course_python.id,
            title="Final quiz",
            translations={"pl": {"title": "Quiz końcowy"}},
            order_index=4,
        )
        db.add(module_py_quiz)
        db.flush()

        lesson_py_quiz = Lesson(
            module_id=module_py_quiz.id,
            title="Final quiz",
            translations={"pl": {"title": "Quiz końcowy"}},
            xp_reward=50,
            is_quiz=True,
        )
        db.add(lesson_py_quiz)
        db.flush()

        db.add_all(
            [
                Exercise(
                    lesson_id=lesson_py_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content="What does print(3 + 4) display?",
                    translations={
                        "pl": {"content": "Co wyświetli print(3 + 4)?", "options": ["7", "3 + 4", "34", "Błąd"]}
                    },
                    correct_answer="7",
                    options=["7", "3 + 4", "34", "An error"],
                ),
                Exercise(
                    lesson_id=lesson_py_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content="Which line creates a variable named age with the value 20?",
                    translations={"pl": {"content": "Która linia tworzy zmienną age o wartości 20?"}},
                    correct_answer="age = 20",
                    options=["age = 20", "20 = age", "age == 20", "var age = 20"],
                ),
                Exercise(
                    lesson_id=lesson_py_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content='What does this code print?\nx = 5\nif x > 3:\n    print("big")\nelse:\n    print("small")',
                    translations={
                        "pl": {
                            "content": 'Co wypisze ten kod?\nx = 5\nif x > 3:\n    print("big")\nelse:\n    print("small")',
                            "options": ["big", "small", "big small", "Nic"],
                        }
                    },
                    correct_answer="big",
                    options=["big", "small", "big small", "Nothing"],
                ),
                Exercise(
                    lesson_id=lesson_py_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content="How many numbers does this loop print?\ni = 0\nwhile i < 3:\n    print(i)\n    i += 1",
                    translations={
                        "pl": {
                            "content": "Ile liczb wypisze ta pętla?\ni = 0\nwhile i < 3:\n    print(i)\n    i += 1",
                            "options": ["3", "2", "4", "Nigdy się nie kończy"],
                        }
                    },
                    correct_answer="3",
                    options=["3", "2", "4", "It never stops"],
                ),
                Exercise(
                    lesson_id=lesson_py_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content='What is fruits[1] if fruits = ["apple", "banana", "cherry"]?',
                    translations={
                        "pl": {
                            "content": 'Ile wynosi fruits[1], jeśli fruits = ["apple", "banana", "cherry"]?',
                            "options": ['"banana"', '"apple"', '"cherry"', "Błąd"],
                        }
                    },
                    correct_answer='"banana"',
                    options=['"banana"', '"apple"', '"cherry"', "An error"],
                ),
                Exercise(
                    lesson_id=lesson_py_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content="What does this loop print?\nfor n in [1, 2, 3]:\n    print(n * 2)",
                    translations={
                        "pl": {
                            "content": "Co wypisze ta pętla?\nfor n in [1, 2, 3]:\n    print(n * 2)",
                            "correct_answer": "2, 4 i 6",
                            "options": ["2, 4 i 6", "1, 2 i 3", "Tylko 6", "2, 2 i 2"],
                        }
                    },
                    correct_answer="2, 4 and 6",
                    options=["2, 4 and 6", "1, 2 and 3", "Only 6", "2, 2 and 2"],
                ),
                Exercise(
                    lesson_id=lesson_py_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content='How do you read the value of the key "name" from person = {"name": "Anna"}?',
                    translations={
                        "pl": {"content": 'Jak odczytać wartość klucza "name" ze słownika person = {"name": "Anna"}?'}
                    },
                    correct_answer='person["name"]',
                    options=['person["name"]', "person[0]", "person.name()", 'person("name")'],
                ),
                Exercise(
                    lesson_id=lesson_py_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content="What does a function return if it has no return statement?",
                    translations={
                        "pl": {
                            "content": "Co zwraca funkcja, która nie ma instrukcji return?",
                            "options": ["None", "0", "Pusty napis", "Powoduje błąd"],
                        }
                    },
                    correct_answer="None",
                    options=["None", "0", "An empty string", "It causes an error"],
                ),
                Exercise(
                    lesson_id=lesson_py_quiz.id,
                    type=ExerciseType.chat,
                    content="In your own words, what is the difference between a list and a dictionary?",
                    translations={"pl": {"content": "Własnymi słowami: czym różni się lista od słownika?"}},
                    correct_answer=(
                        "A list holds ordered items that you access by their numeric index; "
                        "a dictionary holds key-value pairs that you access by key."
                    ),
                ),
                Exercise(
                    lesson_id=lesson_py_quiz.id,
                    type=ExerciseType.chat,
                    content="Why do we write functions instead of copying the same code in several places?",
                    translations={
                        "pl": {"content": "Dlaczego piszemy funkcje zamiast kopiować ten sam kod w kilku miejscach?"}
                    },
                    correct_answer=(
                        "A function lets you write code once and reuse it by calling it, optionally with "
                        "different arguments, so the program is shorter, easier to read and a change is "
                        "made in one place."
                    ),
                ),
            ]
        )

        # =========================================================================
        # Course 2: React Fundamentals
        # =========================================================================
        print("Seeding initial course: 'React Fundamentals'...")
        course_react = Course(
            name="React Fundamentals",
            description=(
                "Master the most popular library for building modern web user interfaces! "
                "Learn functional components, JSX syntax, state management (useState), and side effects (useEffect)."
            ),
            icon_url="https://raw.githubusercontent.com/github/explore/main/topics/react/react.png",
            language="jsx",
            xp_reward=150,
            translations={
                "pl": {
                    "name": "React od podstaw",
                    "description": (
                        "Opanuj najpopularniejszą bibliotekę do tworzenia nowoczesnych interfejsów webowych! "
                        "Poznaj komponenty funkcyjne, składnię JSX, zarządzanie stanem (useState) i efekty uboczne (useEffect)."
                    ),
                }
            },
        )
        db.add(course_react)
        db.flush()

        # -------------------------------------------------------------------------
        # Course 2 / Module 1: Introduction to React and JSX
        # -------------------------------------------------------------------------
        module_react_1 = Module(
            course_id=course_react.id,
            title="Introduction to React and JSX",
            translations={"pl": {"title": "Wprowadzenie do Reacta i JSX"}},
            order_index=1,
        )
        db.add(module_react_1)
        db.flush()

        # Lesson 1.1: What is React and functional components
        lesson_react_1_1 = Lesson(
            module_id=module_react_1.id,
            title="What is React and Components?",
            translations={"pl": {"title": "Czym jest React i komponenty?"}},
            xp_reward=10,
        )
        db.add(lesson_react_1_1)
        db.flush()

        ex_react_9 = Exercise(
            lesson_id=lesson_react_1_1.id,
            type=ExerciseType.multiple_choice,
            content="What does a React component return?",
            translations={
                "pl": {
                    "content": "Co zwraca komponent Reacta?",
                    "correct_answer": "JSX opisujący interfejs",
                    "options": ["JSX opisujący interfejs", "Plik CSS", "Zapytanie do bazy danych"],
                }
            },
            correct_answer="JSX describing the UI",
            options=["JSX describing the UI", "A CSS file", "A database query"],
        )
        db.add(ex_react_9)

        ex_react_1 = Exercise(
            lesson_id=lesson_react_1_1.id,
            type=ExerciseType.code,
            content="Define a functional component named 'Header' that returns an <h1>Welcome to React!</h1> element.",
            translations={
                "pl": {"content": "Zdefiniuj komponent funkcyjny 'Header', który zwraca element <h1>Welcome to React!</h1>."}
            },
            code_snippet='function Header() {\n    return <h1>Welcome to React!</h1>;\n}',
            correct_answer="<h1>Welcome to React!</h1>",
        )
        db.add(ex_react_1)

        # Lesson 1.2: JSX syntax and rendering expressions
        lesson_react_1_2 = Lesson(
            module_id=module_react_1.id,
            title="JSX Syntax and Expressions",
            translations={"pl": {"title": "Składnia JSX i wyrażenia"}},
            xp_reward=15,
        )
        db.add(lesson_react_1_2)
        db.flush()

        ex_react_10 = Exercise(
            lesson_id=lesson_react_1_2.id,
            type=ExerciseType.block_assembly,
            content="Show the title variable inside an h2 element.",
            translations={"pl": {"content": "Wyświetl zmienną title wewnątrz elementu h2."}},
            correct_answer="<h2> {title} </h2>",
            options=["<h2>", "{title}", "</h2>", "{{title}}", "<title>", "$title"],
        )
        db.add(ex_react_10)

        ex_react_2 = Exercise(
            lesson_id=lesson_react_1_2.id,
            type=ExerciseType.code,
            content="Create a constant 'title' with the value \"My Application\", then a constant 'element' with an <h2> that shows title using curly braces {}.",
            translations={
                "pl": {
                    "content": "Utwórz stałą 'title' o wartości \"My Application\", a następnie stałą 'element' z elementem <h2>, który wyświetla title za pomocą nawiasów klamrowych {}."
                }
            },
            code_snippet='const title = "My Application";\nconst element = <h2>{title}</h2>;',
            correct_answer="<h2>{title}</h2>",
        )
        db.add(ex_react_2)

        # Lesson 1.3: Component properties (props)
        lesson_react_1_3 = Lesson(
            module_id=module_react_1.id,
            title="Component Properties (props)",
            translations={"pl": {"title": "Właściwości komponentów (props)"}},
            xp_reward=20,
        )
        db.add(lesson_react_1_3)
        db.flush()

        ex_react_11 = Exercise(
            lesson_id=lesson_react_1_3.id,
            type=ExerciseType.matching,
            content="Match each React concept with its meaning.",
            translations={
                "pl": {
                    "content": "Dopasuj każde pojęcie Reacta do jego znaczenia.",
                    "correct_answer": (
                        "props: Dane przekazane od rodzica; component: Funkcja zwracająca JSX; "
                        "JSX: Składnia podobna do HTML w JavaScripcie"
                    ),
                    "options": [
                        ["props", "Dane przekazane od rodzica"],
                        ["component", "Funkcja zwracająca JSX"],
                        ["JSX", "Składnia podobna do HTML w JavaScripcie"],
                    ],
                }
            },
            correct_answer="props: Data passed from the parent; component: A function that returns JSX; JSX: HTML-like syntax in JavaScript",
            options=[
                ["props", "Data passed from the parent"],
                ["component", "A function that returns JSX"],
                ["JSX", "HTML-like syntax in JavaScript"],
            ],
        )
        db.add(ex_react_11)

        ex_react_3 = Exercise(
            lesson_id=lesson_react_1_3.id,
            type=ExerciseType.code,
            content="Define a component 'Greeting' that receives props and returns <p>Hello, {props.name}!</p>.",
            translations={
                "pl": {"content": "Zdefiniuj komponent 'Greeting', który przyjmuje props i zwraca <p>Hello, {props.name}!</p>."}
            },
            code_snippet='function Greeting(props) {\n    return <p>Hello, {props.name}!</p>;\n}',
            correct_answer="<p>Hello, {props.name}!</p>",
        )
        db.add(ex_react_3)

        # -------------------------------------------------------------------------
        # Course 2 / Module 2: State and Event Handling
        # -------------------------------------------------------------------------
        module_react_2 = Module(
            course_id=course_react.id,
            title="State and Event Handling",
            translations={"pl": {"title": "Stan i obsługa zdarzeń"}},
            order_index=2,
        )
        db.add(module_react_2)
        db.flush()

        # Lesson 2.1: Hook useState
        lesson_react_2_1 = Lesson(
            module_id=module_react_2.id,
            title="useState Hook - Managing State",
            translations={"pl": {"title": "Hook useState – zarządzanie stanem"}},
            xp_reward=20,
        )
        db.add(lesson_react_2_1)
        db.flush()

        ex_react_12 = Exercise(
            lesson_id=lesson_react_2_1.id,
            type=ExerciseType.multiple_choice,
            content="What does useState(0) return?",
            translations={
                "pl": {"content": "Co zwraca useState(0)?", "options": ["[value, setter]", "Liczbę", "Komponent"]}
            },
            correct_answer="[value, setter]",
            options=["[value, setter]", "A number", "A component"],
        )
        db.add(ex_react_12)

        ex_react_4 = Exercise(
            lesson_id=lesson_react_2_1.id,
            type=ExerciseType.code,
            content="Use the useState hook to declare a state variable 'count' initialized to 0 with updater function 'setCount'.",
            translations={
                "pl": {
                    "content": "Użyj hooka useState, aby zadeklarować zmienną stanu 'count' z wartością początkową 0 i funkcją aktualizującą 'setCount'."
                }
            },
            code_snippet="const [count, setCount] = useState(0);",
            correct_answer="const [count, setCount] = useState(0);",
        )
        db.add(ex_react_4)

        # Lesson 2.2: Event handling
        lesson_react_2_2 = Lesson(
            module_id=module_react_2.id,
            title="Handling Events (onClick, onChange)",
            translations={"pl": {"title": "Obsługa zdarzeń (onClick, onChange)"}},
            xp_reward=20,
        )
        db.add(lesson_react_2_2)
        db.flush()

        ex_react_13 = Exercise(
            lesson_id=lesson_react_2_2.id,
            type=ExerciseType.block_assembly,
            content="Call handleClick when the button is clicked.",
            translations={"pl": {"content": "Wywołaj handleClick po kliknięciu przycisku."}},
            correct_answer="<button onClick={handleClick}> Click me </button>",
            options=[
                "<button",
                "onClick={handleClick}>",
                "Click me",
                "</button>",
                'onclick="handleClick()">',
                "onPress={handleClick}>",
            ],
        )
        db.add(ex_react_13)

        ex_react_5 = Exercise(
            lesson_id=lesson_react_2_2.id,
            type=ExerciseType.code,
            content="Create a button <button> that triggers the 'handleClick' function on an onClick event.",
            translations={
                "pl": {"content": "Utwórz przycisk <button>, który wywołuje funkcję 'handleClick' przy zdarzeniu onClick."}
            },
            code_snippet="<button onClick={handleClick}>Click me</button>",
            correct_answer="<button onClick={handleClick}>Click me</button>",
        )
        db.add(ex_react_5)

        # Lesson 2.3: Conditional rendering
        lesson_react_2_3 = Lesson(
            module_id=module_react_2.id,
            title="Conditional Component Rendering",
            translations={"pl": {"title": "Warunkowe renderowanie komponentów"}},
            xp_reward=25,
        )
        db.add(lesson_react_2_3)
        db.flush()

        ex_react_14 = Exercise(
            lesson_id=lesson_react_2_3.id,
            type=ExerciseType.multiple_choice,
            content="Which expression renders one of two elements based on a condition?",
            translations={
                "pl": {"content": "Które wyrażenie renderuje jeden z dwóch elementów w zależności od warunku?"}
            },
            correct_answer="condition ? a : b",
            options=["condition ? a : b", "condition => a : b", "if (condition) a else b"],
        )
        db.add(ex_react_14)

        ex_react_6 = Exercise(
            lesson_id=lesson_react_2_3.id,
            type=ExerciseType.code,
            content="Use a ternary operator in JSX to render <p>Logged in</p> when 'isLoggedIn' is true, and <p>Please log in</p> otherwise.",
            translations={
                "pl": {
                    "content": "Użyj operatora trójargumentowego w JSX, aby wyrenderować <p>Logged in</p>, gdy 'isLoggedIn' jest prawdą, a w przeciwnym razie <p>Please log in</p>."
                }
            },
            code_snippet="{isLoggedIn ? <p>Logged in</p> : <p>Please log in</p>}",
            correct_answer="{isLoggedIn ? <p>Logged in</p> : <p>Please log in</p>}",
        )
        db.add(ex_react_6)

        # -------------------------------------------------------------------------
        # Course 2 / Module 3: Side Effects and API Integration
        # -------------------------------------------------------------------------
        module_react_3 = Module(
            course_id=course_react.id,
            title="Side Effects and API Integration",
            translations={"pl": {"title": "Efekty uboczne i integracja z API"}},
            order_index=3,
        )
        db.add(module_react_3)
        db.flush()

        # Lesson 3.1: Hook useEffect
        lesson_react_3_1 = Lesson(
            module_id=module_react_3.id,
            title="useEffect Hook and Component Lifecycle",
            translations={"pl": {"title": "Hook useEffect i cykl życia komponentu"}},
            xp_reward=25,
        )
        db.add(lesson_react_3_1)
        db.flush()

        ex_react_15 = Exercise(
            lesson_id=lesson_react_3_1.id,
            type=ExerciseType.matching,
            content="Match the dependency array with when the effect runs.",
            translations={
                "pl": {
                    "content": "Dopasuj tablicę zależności do momentu uruchomienia efektu.",
                    "correct_answer": (
                        "[]: Raz, po pierwszym renderze; [count]: Gdy zmieni się count; "
                        "brak tablicy: Po każdym renderze"
                    ),
                    "options": [
                        ["[]", "Raz, po pierwszym renderze"],
                        ["[count]", "Gdy zmieni się count"],
                        ["brak tablicy", "Po każdym renderze"],
                    ],
                }
            },
            correct_answer="[]: Once, after the first render; [count]: When count changes; no array: After every render",
            options=[
                ["[]", "Once, after the first render"],
                ["[count]", "When count changes"],
                ["no array", "After every render"],
            ],
        )
        db.add(ex_react_15)

        ex_react_7 = Exercise(
            lesson_id=lesson_react_3_1.id,
            type=ExerciseType.code,
            content="Use the useEffect hook with an empty dependency array [] to log 'Component mounted' to the console only once on mount.",
            translations={
                "pl": {
                    "content": "Użyj hooka useEffect z pustą tablicą zależności [], aby tylko raz, po zamontowaniu, wypisać w konsoli 'Component mounted'."
                }
            },
            code_snippet='useEffect(() => {\n    console.log("Component mounted");\n}, []);',
            correct_answer='useEffect(() => {\n    console.log("Component mounted");\n}, []);',
        )
        db.add(ex_react_7)

        # Lesson 3.2: Fetching data in useEffect
        lesson_react_3_2 = Lesson(
            module_id=module_react_3.id,
            title="Fetching Data in useEffect",
            translations={"pl": {"title": "Pobieranie danych w useEffect"}},
            xp_reward=30,
        )
        db.add(lesson_react_3_2)
        db.flush()

        ex_react_16 = Exercise(
            lesson_id=lesson_react_3_2.id,
            type=ExerciseType.multiple_choice,
            content="Where should a function component fetch data?",
            translations={
                "pl": {
                    "content": "Gdzie komponent funkcyjny powinien pobierać dane?",
                    "correct_answer": "Wewnątrz useEffect",
                    "options": ["Wewnątrz useEffect", "Bezpośrednio w instrukcji return", "Wewnątrz useState"],
                }
            },
            correct_answer="Inside useEffect",
            options=["Inside useEffect", "Directly in the return statement", "Inside useState"],
        )
        db.add(ex_react_16)

        ex_react_8 = Exercise(
            lesson_id=lesson_react_3_2.id,
            type=ExerciseType.code,
            content="Inside useEffect, call fetch('/api/courses') to retrieve course data from the server.",
            translations={
                "pl": {"content": "Wewnątrz useEffect wywołaj fetch('/api/courses'), aby pobrać dane kursów z serwera."}
            },
            code_snippet='useEffect(() => {\n    fetch("/api/courses");\n}, []);',
            correct_answer='fetch("/api/courses")',
        )
        db.add(ex_react_8)

        module_react_quiz = Module(
            course_id=course_react.id,
            title="Final quiz",
            translations={"pl": {"title": "Quiz końcowy"}},
            order_index=4,
        )
        db.add(module_react_quiz)
        db.flush()

        lesson_react_quiz = Lesson(
            module_id=module_react_quiz.id,
            title="Final quiz",
            translations={"pl": {"title": "Quiz końcowy"}},
            xp_reward=50,
            is_quiz=True,
        )
        db.add(lesson_react_quiz)
        db.flush()

        db.add_all(
            [
                Exercise(
                    lesson_id=lesson_react_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content="What is a React component?",
                    translations={
                        "pl": {
                            "content": "Czym jest komponent Reacta?",
                            "correct_answer": "Funkcja, która zwraca JSX opisujący część interfejsu",
                            "options": [
                                "Funkcja, która zwraca JSX opisujący część interfejsu",
                                "Plik CSS ze stylami",
                                "Tabela w bazie danych",
                                "Plik HTML wczytywany przez przeglądarkę",
                            ],
                        }
                    },
                    correct_answer="A function that returns JSX describing part of the UI",
                    options=[
                        "A function that returns JSX describing part of the UI",
                        "A CSS file with styles",
                        "A database table",
                        "An HTML file loaded by the browser",
                    ],
                ),
                Exercise(
                    lesson_id=lesson_react_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content="How do you show the value of the variable name inside JSX?",
                    translations={"pl": {"content": "Jak wyświetlić wartość zmiennej name w JSX?"}},
                    correct_answer="{name}",
                    options=["{name}", "${name}", "{{name}}", "(name)"],
                ),
                Exercise(
                    lesson_id=lesson_react_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content="How does a parent component pass data to a child component?",
                    translations={
                        "pl": {
                            "content": "Jak komponent rodzica przekazuje dane do komponentu dziecka?",
                            "correct_answer": 'Przez props, np. <Child title="Hi" />',
                            "options": [
                                'Przez props, np. <Child title="Hi" />',
                                "Przez zmienną globalną",
                                "Wywołując bezpośrednio funkcję dziecka",
                                "Przez useEffect",
                            ],
                        }
                    },
                    correct_answer='With props, like <Child title="Hi" />',
                    options=[
                        'With props, like <Child title="Hi" />',
                        "With a global variable",
                        "By calling the child function directly",
                        "With useEffect",
                    ],
                ),
                Exercise(
                    lesson_id=lesson_react_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content="What does const [count, setCount] = useState(0) give you?",
                    translations={
                        "pl": {
                            "content": "Co daje const [count, setCount] = useState(0)?",
                            "correct_answer": "Aktualną wartość i funkcję do jej zmiany",
                            "options": [
                                "Aktualną wartość i funkcję do jej zmiany",
                                "Dwie kopie wartości 0",
                                "Funkcję i jej wynik",
                                "Listę z jednym elementem",
                            ],
                        }
                    },
                    correct_answer="The current value and a function to update it",
                    options=[
                        "The current value and a function to update it",
                        "Two copies of the value 0",
                        "A function and its return value",
                        "A list with one element",
                    ],
                ),
                Exercise(
                    lesson_id=lesson_react_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content="Which attribute runs handleClick when a button is clicked?",
                    translations={"pl": {"content": "Który atrybut wywołuje handleClick po kliknięciu przycisku?"}},
                    correct_answer="onClick={handleClick}",
                    options=[
                        "onClick={handleClick}",
                        'onclick="handleClick()"',
                        "click={handleClick}",
                        "onPress={handleClick}",
                    ],
                ),
                Exercise(
                    lesson_id=lesson_react_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content="What does {isLoggedIn ? <Profile /> : <Login />} render when isLoggedIn is false?",
                    translations={
                        "pl": {
                            "content": "Co wyrenderuje {isLoggedIn ? <Profile /> : <Login />}, gdy isLoggedIn ma wartość false?",
                            "options": ["<Login />", "<Profile />", "Oba komponenty", "Nic"],
                        }
                    },
                    correct_answer="<Login />",
                    options=["<Login />", "<Profile />", "Both components", "Nothing"],
                ),
                Exercise(
                    lesson_id=lesson_react_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content="When does useEffect(() => { ... }, []) run?",
                    translations={
                        "pl": {
                            "content": "Kiedy uruchamia się useEffect(() => { ... }, [])?",
                            "correct_answer": "Raz, po pierwszym renderze",
                            "options": [
                                "Raz, po pierwszym renderze",
                                "Po każdym renderze",
                                "Przed pierwszym renderem",
                                "Tylko po kliknięciu przez użytkownika",
                            ],
                        }
                    },
                    correct_answer="Once, after the first render",
                    options=[
                        "Once, after the first render",
                        "After every render",
                        "Before the first render",
                        "Only when the user clicks",
                    ],
                ),
                Exercise(
                    lesson_id=lesson_react_quiz.id,
                    type=ExerciseType.multiple_choice,
                    content="Where should a function component start fetching data from an API?",
                    translations={
                        "pl": {
                            "content": "Gdzie komponent funkcyjny powinien zacząć pobieranie danych z API?",
                            "correct_answer": "Wewnątrz useEffect",
                            "options": ["Wewnątrz useEffect", "Bezpośrednio w JSX", "Wewnątrz useState", "W pliku CSS"],
                        }
                    },
                    correct_answer="Inside useEffect",
                    options=["Inside useEffect", "Directly in the JSX", "Inside useState", "In the CSS file"],
                ),
                Exercise(
                    lesson_id=lesson_react_quiz.id,
                    type=ExerciseType.chat,
                    content="Why do we store a counter with useState instead of a normal variable?",
                    translations={
                        "pl": {"content": "Dlaczego licznik przechowujemy w useState, a nie w zwykłej zmiennej?"}
                    },
                    correct_answer=(
                        "Calling the state setter makes React re-render the component with the new value; "
                        "changing a normal variable doesn't trigger a re-render and the variable is reset "
                        "on every render."
                    ),
                ),
                Exercise(
                    lesson_id=lesson_react_quiz.id,
                    type=ExerciseType.chat,
                    content="Why does useEffect take a dependency array, and what happens when it is empty?",
                    translations={
                        "pl": {"content": "Po co useEffect przyjmuje tablicę zależności i co się dzieje, gdy jest pusta?"}
                    },
                    correct_answer=(
                        "The dependency array tells React when to run the effect again: only when one of "
                        "the listed values changes. With an empty array the effect runs only once, after "
                        "the first render."
                    ),
                ),
            ]
        )

        db.commit()
        print(
            f"Database successfully seeded! Created courses 'Python Basics' (ID: {course_python.id}) "
            f"and 'React Fundamentals' (ID: {course_react.id}) with complete module, lesson, and exercise hierarchies."
        )
        seed_track_courses(db, force=force)
    except Exception as e:
        db.rollback()
        print(f"Error occurred while seeding the database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    force_flag = "--force" in sys.argv
    seed_database(force=force_flag)
