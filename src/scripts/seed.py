"""Database seeding script for code-learner.

Populates the database with initial courses, modules, lessons, and Dual Mode coding exercises.
Run via:
    uv run python -m src.scripts.seed
or
    make seed
"""

import sys

from src.model.course import Course
from src.model.db import SessionLocal
from src.model.exercise import Exercise, ExerciseType
from src.model.lesson import Lesson
from src.model.module import Module


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
        )
        db.add(course_python)
        db.flush()

        # -------------------------------------------------------------------------
        # Course 1 / Module 1: First Steps in Python
        # -------------------------------------------------------------------------
        module_py_1 = Module(
            course_id=course_python.id,
            title="First Steps in Python",
            order_index=1,
        )
        db.add(module_py_1)
        db.flush()

        # Lesson 1.1: Printing text and variables
        lesson_py_1_1 = Lesson(
            module_id=module_py_1.id,
            title="Printing Text and Variables",
            xp_reward=10,
        )
        db.add(lesson_py_1_1)
        db.flush()

        ex_py_10 = Exercise(
            lesson_id=lesson_py_1_1.id,
            type=ExerciseType.block_assembly,
            content='Display the text "Hello Polycode" on the screen.',
            correct_answer='print ( "Hello Polycode" )',
            options=["print", "(", '"Hello Polycode"', ")", ";", "cout", "[", "]", "echo"],
        )
        db.add(ex_py_10)

        ex_py_1 = Exercise(
            lesson_id=lesson_py_1_1.id,
            type=ExerciseType.code,
            content='Write a program that prints "Hello, World!" to the console.',
            code_snippet='print("Hello, World!")',
            correct_answer="Hello, World!",
        )
        ex_py_2 = Exercise(
            lesson_id=lesson_py_1_1.id,
            type=ExerciseType.code,
            content='Create a variable named name with the value "John" and print it using the print function.',
            code_snippet='name = "John"\nprint(name)',
            correct_answer="John",
        )
        db.add_all([ex_py_1, ex_py_2])

        # Five questions per lesson, as in Figma (progress moves in 20% steps).
        ex_py_18 = Exercise(
            lesson_id=lesson_py_1_1.id,
            type=ExerciseType.multiple_choice,
            content="Which function displays text on the screen in Python?",
            correct_answer="print()",
            options=["print()", "echo()", "console.log()"],
        )
        ex_py_19 = Exercise(
            lesson_id=lesson_py_1_1.id,
            type=ExerciseType.multiple_choice,
            content='Which line stores the text "Duck" in a variable named pet?',
            correct_answer='pet = "Duck"',
            options=['pet = "Duck"', '"Duck" = pet', 'pet == "Duck"'],
        )
        db.add_all([ex_py_18, ex_py_19])

        # Lesson 1.2: Conditional statements
        lesson_py_1_2 = Lesson(
            module_id=module_py_1.id,
            title="Conditional Statements (if / else)",
            xp_reward=15,
        )
        db.add(lesson_py_1_2)
        db.flush()

        ex_py_11 = Exercise(
            lesson_id=lesson_py_1_2.id,
            type=ExerciseType.multiple_choice,
            content="Which keyword runs code when the if condition is false?",
            correct_answer="else",
            options=["else", "otherwise", "then"],
        )
        db.add(ex_py_11)

        ex_py_3 = Exercise(
            lesson_id=lesson_py_1_2.id,
            type=ExerciseType.code,
            content=(
                "Check if the variable 'score' is greater than or equal to 50. "
                "If so, print 'Pass', otherwise print 'Retake'."
            ),
            code_snippet='score = 75\nif score >= 50:\n    print("Pass")\nelse:\n    print("Retake")',
            correct_answer="Pass",
        )
        db.add(ex_py_3)

        # Lesson 1.3: While loops and basic operations
        lesson_py_1_3 = Lesson(
            module_id=module_py_1.id,
            title="While Loops and Logical Operators",
            xp_reward=15,
        )
        db.add(lesson_py_1_3)
        db.flush()

        ex_py_12 = Exercise(
            lesson_id=lesson_py_1_3.id,
            type=ExerciseType.multiple_choice,
            content="Which operator means 'and' in Python?",
            correct_answer="and",
            options=["and", "&&", "&"],
        )
        db.add(ex_py_12)

        ex_py_4 = Exercise(
            lesson_id=lesson_py_1_3.id,
            type=ExerciseType.code,
            content="Write a while loop that prints numbers from 1 to 3.",
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
            order_index=2,
        )
        db.add(module_py_2)
        db.flush()

        # Lesson 2.1: Lists and indexing
        lesson_py_2_1 = Lesson(
            module_id=module_py_2.id,
            title="Lists and Indexing Elements",
            xp_reward=20,
        )
        db.add(lesson_py_2_1)
        db.flush()

        ex_py_13 = Exercise(
            lesson_id=lesson_py_2_1.id,
            type=ExerciseType.multiple_choice,
            content="Which represents an empty list in Python?",
            correct_answer="[ ]",
            options=["[ ]", "( )", "{ }"],
        )
        db.add(ex_py_13)

        ex_py_5 = Exercise(
            lesson_id=lesson_py_2_1.id,
            type=ExerciseType.code,
            content="Create a list named 'fruits' containing 'apple' and 'banana', then print its first element.",
            code_snippet='fruits = ["apple", "banana"]\nprint(fruits[0])',
            correct_answer="apple",
        )
        db.add(ex_py_5)

        # Lesson 2.2: For loop and iteration
        lesson_py_2_2 = Lesson(
            module_id=module_py_2.id,
            title="For Loops and Iteration",
            xp_reward=20,
        )
        db.add(lesson_py_2_2)
        db.flush()

        ex_py_14 = Exercise(
            lesson_id=lesson_py_2_2.id,
            type=ExerciseType.block_assembly,
            content="Build a loop that goes over every number in the list numbers.",
            correct_answer="for number in numbers :",
            options=["for", "number", "in", "numbers", ":", "each", "of", ";"],
        )
        db.add(ex_py_14)

        ex_py_6 = Exercise(
            lesson_id=lesson_py_2_2.id,
            type=ExerciseType.code,
            content="Use a for loop to print every number from the list [1, 2, 3].",
            code_snippet='numbers = [1, 2, 3]\nfor number in numbers:\n    print(number)',
            correct_answer="1\n2\n3",
        )
        db.add(ex_py_6)

        # Lesson 2.3: Dictionaries and key-value pairs
        lesson_py_2_3 = Lesson(
            module_id=module_py_2.id,
            title="Dictionaries and Key-Value Pairs",
            xp_reward=25,
        )
        db.add(lesson_py_2_3)
        db.flush()

        ex_py_15 = Exercise(
            lesson_id=lesson_py_2_3.id,
            type=ExerciseType.matching,
            content="Select the matching pairs.",
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
            order_index=3,
        )
        db.add(module_py_3)
        db.flush()

        # Lesson 3.1: Defining custom functions
        lesson_py_3_1 = Lesson(
            module_id=module_py_3.id,
            title="Defining Functions (def)",
            xp_reward=25,
        )
        db.add(lesson_py_3_1)
        db.flush()

        ex_py_16 = Exercise(
            lesson_id=lesson_py_3_1.id,
            type=ExerciseType.block_assembly,
            content="Start the definition of a function named greet.",
            correct_answer="def greet ( ) :",
            options=["def", "greet", "(", ")", ":", "function", "{", "fn"],
        )
        db.add(ex_py_16)

        ex_py_8 = Exercise(
            lesson_id=lesson_py_3_1.id,
            type=ExerciseType.code,
            content="Define a function named 'greet()' that prints 'Hello!'. Call this function.",
            code_snippet='def greet():\n    print("Hello!")\n\ngreet()',
            correct_answer="Hello!",
        )
        db.add(ex_py_8)

        # Lesson 3.2: Parameters and return values
        lesson_py_3_2 = Lesson(
            module_id=module_py_3.id,
            title="Parameters and Return Values (return)",
            xp_reward=30,
        )
        db.add(lesson_py_3_2)
        db.flush()

        ex_py_17 = Exercise(
            lesson_id=lesson_py_3_2.id,
            type=ExerciseType.multiple_choice,
            content="Which keyword sends a value back from a function?",
            correct_answer="return",
            options=["return", "print", "send"],
        )
        db.add(ex_py_17)

        ex_py_9 = Exercise(
            lesson_id=lesson_py_3_2.id,
            type=ExerciseType.code,
            content="Write a function 'add(a, b)' that returns the sum of two numbers. Print the result of add(2, 3).",
            code_snippet='def add(a, b):\n    return a + b\n\nprint(add(2, 3))',
            correct_answer="5",
        )
        db.add(ex_py_9)

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
        )
        db.add(course_react)
        db.flush()

        # -------------------------------------------------------------------------
        # Course 2 / Module 1: Introduction to React and JSX
        # -------------------------------------------------------------------------
        module_react_1 = Module(
            course_id=course_react.id,
            title="Introduction to React and JSX",
            order_index=1,
        )
        db.add(module_react_1)
        db.flush()

        # Lesson 1.1: What is React and functional components
        lesson_react_1_1 = Lesson(
            module_id=module_react_1.id,
            title="What is React and Components?",
            xp_reward=10,
        )
        db.add(lesson_react_1_1)
        db.flush()

        ex_react_9 = Exercise(
            lesson_id=lesson_react_1_1.id,
            type=ExerciseType.multiple_choice,
            content="What does a React component return?",
            correct_answer="JSX describing the UI",
            options=["JSX describing the UI", "A CSS file", "A database query"],
        )
        db.add(ex_react_9)

        ex_react_1 = Exercise(
            lesson_id=lesson_react_1_1.id,
            type=ExerciseType.code,
            content="Define a functional component named 'Header' that returns an <h1>Welcome to React!</h1> element.",
            code_snippet='function Header() {\n    return <h1>Welcome to React!</h1>;\n}',
            correct_answer="<h1>Welcome to React!</h1>",
        )
        db.add(ex_react_1)

        # Lesson 1.2: JSX syntax and rendering expressions
        lesson_react_1_2 = Lesson(
            module_id=module_react_1.id,
            title="JSX Syntax and Expressions",
            xp_reward=15,
        )
        db.add(lesson_react_1_2)
        db.flush()

        ex_react_10 = Exercise(
            lesson_id=lesson_react_1_2.id,
            type=ExerciseType.block_assembly,
            content="Show the title variable inside an h2 element.",
            correct_answer="<h2> {title} </h2>",
            options=["<h2>", "{title}", "</h2>", "{{title}}", "<title>", "$title"],
        )
        db.add(ex_react_10)

        ex_react_2 = Exercise(
            lesson_id=lesson_react_1_2.id,
            type=ExerciseType.code,
            content="Embed the JavaScript variable 'title' inside an <h2> element using curly braces {}.",
            code_snippet='const title = "My Application";\nconst element = <h2>{title}</h2>;',
            correct_answer="<h2>{title}</h2>",
        )
        db.add(ex_react_2)

        # Lesson 1.3: Component properties (props)
        lesson_react_1_3 = Lesson(
            module_id=module_react_1.id,
            title="Component Properties (props)",
            xp_reward=20,
        )
        db.add(lesson_react_1_3)
        db.flush()

        ex_react_11 = Exercise(
            lesson_id=lesson_react_1_3.id,
            type=ExerciseType.matching,
            content="Match each React concept with its meaning.",
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
            order_index=2,
        )
        db.add(module_react_2)
        db.flush()

        # Lesson 2.1: Hook useState
        lesson_react_2_1 = Lesson(
            module_id=module_react_2.id,
            title="useState Hook - Managing State",
            xp_reward=20,
        )
        db.add(lesson_react_2_1)
        db.flush()

        ex_react_12 = Exercise(
            lesson_id=lesson_react_2_1.id,
            type=ExerciseType.multiple_choice,
            content="What does useState(0) return?",
            correct_answer="[value, setter]",
            options=["[value, setter]", "A number", "A component"],
        )
        db.add(ex_react_12)

        ex_react_4 = Exercise(
            lesson_id=lesson_react_2_1.id,
            type=ExerciseType.code,
            content="Use the useState hook to declare a state variable 'count' initialized to 0 with updater function 'setCount'.",
            code_snippet="const [count, setCount] = useState(0);",
            correct_answer="const [count, setCount] = useState(0);",
        )
        db.add(ex_react_4)

        # Lesson 2.2: Event handling
        lesson_react_2_2 = Lesson(
            module_id=module_react_2.id,
            title="Handling Events (onClick, onChange)",
            xp_reward=20,
        )
        db.add(lesson_react_2_2)
        db.flush()

        ex_react_13 = Exercise(
            lesson_id=lesson_react_2_2.id,
            type=ExerciseType.block_assembly,
            content="Call handleClick when the button is clicked.",
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
            code_snippet="<button onClick={handleClick}>Click me</button>",
            correct_answer="<button onClick={handleClick}>Click me</button>",
        )
        db.add(ex_react_5)

        # Lesson 2.3: Conditional rendering
        lesson_react_2_3 = Lesson(
            module_id=module_react_2.id,
            title="Conditional Component Rendering",
            xp_reward=25,
        )
        db.add(lesson_react_2_3)
        db.flush()

        ex_react_14 = Exercise(
            lesson_id=lesson_react_2_3.id,
            type=ExerciseType.multiple_choice,
            content="Which expression renders one of two elements based on a condition?",
            correct_answer="condition ? a : b",
            options=["condition ? a : b", "condition => a : b", "if (condition) a else b"],
        )
        db.add(ex_react_14)

        ex_react_6 = Exercise(
            lesson_id=lesson_react_2_3.id,
            type=ExerciseType.code,
            content="Use a ternary operator in JSX to render <p>Logged in</p> when 'isLoggedIn' is true, and <p>Please log in</p> otherwise.",
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
            order_index=3,
        )
        db.add(module_react_3)
        db.flush()

        # Lesson 3.1: Hook useEffect
        lesson_react_3_1 = Lesson(
            module_id=module_react_3.id,
            title="useEffect Hook and Component Lifecycle",
            xp_reward=25,
        )
        db.add(lesson_react_3_1)
        db.flush()

        ex_react_15 = Exercise(
            lesson_id=lesson_react_3_1.id,
            type=ExerciseType.matching,
            content="Match the dependency array with when the effect runs.",
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
            code_snippet='useEffect(() => {\n    console.log("Component mounted");\n}, []);',
            correct_answer='useEffect(() => {\n    console.log("Component mounted");\n}, []);',
        )
        db.add(ex_react_7)

        # Lesson 3.2: Fetching data in useEffect
        lesson_react_3_2 = Lesson(
            module_id=module_react_3.id,
            title="Fetching Data in useEffect",
            xp_reward=30,
        )
        db.add(lesson_react_3_2)
        db.flush()

        ex_react_16 = Exercise(
            lesson_id=lesson_react_3_2.id,
            type=ExerciseType.multiple_choice,
            content="Where should a function component fetch data?",
            correct_answer="Inside useEffect",
            options=["Inside useEffect", "Directly in the return statement", "Inside useState"],
        )
        db.add(ex_react_16)

        ex_react_8 = Exercise(
            lesson_id=lesson_react_3_2.id,
            type=ExerciseType.code,
            content="Inside useEffect, call fetch('/api/courses') to retrieve course data from the server.",
            code_snippet='useEffect(() => {\n    fetch("/api/courses");\n}, []);',
            correct_answer='fetch("/api/courses")',
        )
        db.add(ex_react_8)

        db.commit()
        print(
            f"Database successfully seeded! Created courses 'Python Basics' (ID: {course_python.id}) "
            f"and 'React Fundamentals' (ID: {course_react.id}) with complete module, lesson, and exercise hierarchies."
        )
    except Exception as e:
        db.rollback()
        print(f"Error occurred while seeding the database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    force_flag = "--force" in sys.argv
    seed_database(force=force_flag)
