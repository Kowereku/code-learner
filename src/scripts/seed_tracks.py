"""Sample courses for the learning areas picked on the Choice page.

Each area gets at least one course: Python Basics (seed.py) and Data Analysis with
Python cover Data Science & AI, Linux Command Line Basics covers Essentials of Linux
and Java Basics covers Backend Engineering. Called from seed.py, so ``make seed``
adds whichever of these courses are still missing.
"""

from sqlalchemy.orm import Session

from src.model.course import Course, Track
from src.model.exercise import Exercise, ExerciseType
from src.model.lesson import Lesson
from src.model.module import Module


def quiz_module(order_index: int, exercises: list[Exercise]) -> Module:
    """The closing module every course ends with: one final quiz lesson."""
    return Module(
        title="Final quiz",
        translations={"pl": {"title": "Quiz końcowy"}},
        order_index=order_index,
        lessons=[
            Lesson(
                title="Final quiz",
                translations={"pl": {"title": "Quiz końcowy"}},
                xp_reward=50,
                is_quiz=True,
                exercises=exercises,
            )
        ],
    )


# =============================================================================
# Data Science & AI: Data Analysis with Python
# =============================================================================
def data_analysis_course() -> Course:
    return Course(
        name="Data Analysis with Python",
        description=(
            "Turn lists of numbers into answers! Count, sum, average and filter data "
            "with plain Python, the first step towards data science and AI."
        ),
        icon_url="https://raw.githubusercontent.com/github/explore/main/topics/pandas/pandas.png",
        language="python",
        track=Track.data_science,
        xp_reward=150,
        translations={
            "pl": {
                "name": "Analiza danych w Pythonie",
                "description": (
                    "Zamień listy liczb w odpowiedzi! Zliczaj, sumuj, licz średnie i filtruj dane "
                    "w czystym Pythonie, to pierwszy krok w stronę data science i AI."
                ),
            }
        },
        modules=[
            Module(
                title="Working with Data",
                translations={"pl": {"title": "Praca z danymi"}},
                order_index=1,
                lessons=[
                    Lesson(
                        title="Lists of Data",
                        translations={"pl": {"title": "Listy danych"}},
                        xp_reward=10,
                        exercises=[
                            Exercise(
                                type=ExerciseType.multiple_choice,
                                content="Which function returns the number of items in a list?",
                                translations={"pl": {"content": "Która funkcja zwraca liczbę elementów listy?"}},
                                correct_answer="len()",
                                options=["len()", "count()", "size()", "length()"],
                            ),
                            Exercise(
                                type=ExerciseType.block_assembly,
                                content="Add up all the values in the list scores and store the result in total.",
                                translations={
                                    "pl": {"content": "Zsumuj wszystkie wartości z listy scores i zapisz wynik w total."}
                                },
                                correct_answer="total = sum ( scores )",
                                options=["total", "=", "sum", "(", "scores", ")", "add", "+=", "len"],
                            ),
                            Exercise(
                                type=ExerciseType.code,
                                content="Create a list numbers with the values 4, 8 and 15, then print their sum.",
                                translations={
                                    "pl": {"content": "Utwórz listę numbers z wartościami 4, 8 i 15, a potem wypisz ich sumę."}
                                },
                                code_snippet="numbers = [4, 8, 15]\nprint(sum(numbers))",
                                correct_answer="27",
                            ),
                        ],
                    ),
                    Lesson(
                        title="Averages and Statistics",
                        translations={"pl": {"title": "Średnie i statystyki"}},
                        xp_reward=10,
                        exercises=[
                            Exercise(
                                type=ExerciseType.matching,
                                content="Match each function with what it returns for a list of numbers.",
                                translations={
                                    "pl": {
                                        "content": "Dopasuj każdą funkcję do tego, co zwraca dla listy liczb.",
                                        "correct_answer": (
                                            "sum(): suma wszystkich wartości; len(): liczba elementów; "
                                            "max(): największa wartość; min(): najmniejsza wartość"
                                        ),
                                        "options": [
                                            ["sum()", "Suma wszystkich wartości"],
                                            ["len()", "Liczba elementów"],
                                            ["max()", "Największa wartość"],
                                            ["min()", "Najmniejsza wartość"],
                                        ],
                                    }
                                },
                                correct_answer=(
                                    "sum(): total of all values; len(): number of items; "
                                    "max(): largest value; min(): smallest value"
                                ),
                                options=[
                                    ["sum()", "Total of all values"],
                                    ["len()", "Number of items"],
                                    ["max()", "Largest value"],
                                    ["min()", "Smallest value"],
                                ],
                            ),
                            Exercise(
                                type=ExerciseType.code,
                                content="Create a list values with 2, 4 and 6, then print their average.",
                                translations={
                                    "pl": {"content": "Utwórz listę values z liczbami 2, 4 i 6, a potem wypisz ich średnią."}
                                },
                                code_snippet="values = [2, 4, 6]\nprint(sum(values) / len(values))",
                                correct_answer="4.0",
                            ),
                            Exercise(
                                type=ExerciseType.multiple_choice,
                                content="What is the median of the sorted list [1, 3, 9]?",
                                translations={"pl": {"content": "Jaka jest mediana posortowanej listy [1, 3, 9]?"}},
                                correct_answer="3",
                                options=["3", "4.33", "9", "1"],
                            ),
                        ],
                    ),
                    Lesson(
                        title="Filtering Data",
                        translations={"pl": {"title": "Filtrowanie danych"}},
                        xp_reward=10,
                        exercises=[
                            Exercise(
                                type=ExerciseType.multiple_choice,
                                content="What does data[0] return?",
                                translations={
                                    "pl": {
                                        "content": "Co zwraca data[0]?",
                                        "correct_answer": "Pierwszy element listy",
                                        "options": [
                                            "Pierwszy element listy",
                                            "Ostatni element listy",
                                            "Liczbę elementów listy",
                                            "Pustą listę",
                                        ],
                                    }
                                },
                                correct_answer="The first item of the list",
                                options=[
                                    "The first item of the list",
                                    "The last item of the list",
                                    "The number of items",
                                    "An empty list",
                                ],
                            ),
                            Exercise(
                                type=ExerciseType.block_assembly,
                                content="Build a list with only the values from data that are greater than 10.",
                                translations={
                                    "pl": {"content": "Zbuduj listę zawierającą tylko te wartości z data, które są większe od 10."}
                                },
                                correct_answer="[ x for x in data if x > 10 ]",
                                options=["[", "x", "for", "x", "in", "data", "if", "x", ">", "10", "]", "where", "<"],
                            ),
                            Exercise(
                                type=ExerciseType.code,
                                content="Create a list data with 3, 7 and 9, then print only the values greater than 5.",
                                translations={
                                    "pl": {
                                        "content": "Utwórz listę data z liczbami 3, 7 i 9, a potem wypisz tylko wartości większe od 5."
                                    }
                                },
                                code_snippet="data = [3, 7, 9]\nprint([x for x in data if x > 5])",
                                correct_answer="[7, 9]",
                            ),
                        ],
                    ),
                ],
            ),
            quiz_module(
                2,
                [
                    Exercise(
                        type=ExerciseType.multiple_choice,
                        content="What does sum([1, 2, 3]) return?",
                        translations={"pl": {"content": "Co zwraca sum([1, 2, 3])?"}},
                        correct_answer="6",
                        options=["6", "3", "123", "[1, 2, 3]"],
                    ),
                    Exercise(
                        type=ExerciseType.multiple_choice,
                        content="How do you calculate the average of the list values?",
                        translations={"pl": {"content": "Jak obliczyć średnią z listy values?"}},
                        correct_answer="sum(values) / len(values)",
                        options=[
                            "sum(values) / len(values)",
                            "len(values) / sum(values)",
                            "max(values) - min(values)",
                            "average(values)",
                        ],
                    ),
                    Exercise(
                        type=ExerciseType.multiple_choice,
                        content="What does max([5, 12, 7]) return?",
                        translations={"pl": {"content": "Co zwraca max([5, 12, 7])?"}},
                        correct_answer="12",
                        options=["12", "5", "7", "24"],
                    ),
                    Exercise(
                        type=ExerciseType.multiple_choice,
                        content="What is the result of [x for x in [1, 6, 8] if x > 5]?",
                        translations={"pl": {"content": "Jaki jest wynik [x for x in [1, 6, 8] if x > 5]?"}},
                        correct_answer="[6, 8]",
                        options=["[6, 8]", "[1]", "[1, 6, 8]", "2"],
                    ),
                    Exercise(
                        type=ExerciseType.chat,
                        content="Why is the median sometimes a better summary of data than the average?",
                        translations={
                            "pl": {"content": "Dlaczego mediana bywa lepszym podsumowaniem danych niż średnia?"}
                        },
                        correct_answer=(
                            "The average is pulled towards a few very large or very small values (outliers), "
                            "while the median is the middle value, so it still shows a typical value when the "
                            "data has outliers."
                        ),
                    ),
                ],
            ),
        ],
    )


# =============================================================================
# Essentials of Linux: Linux Command Line Basics
# =============================================================================
def linux_course() -> Course:
    return Course(
        name="Linux Command Line Basics",
        description=(
            "Get comfortable in the terminal! Move around the file system, manage files "
            "and understand permissions, the foundation of secure systems."
        ),
        icon_url="https://raw.githubusercontent.com/github/explore/main/topics/linux/linux.png",
        language="bash",
        track=Track.linux,
        xp_reward=150,
        translations={
            "pl": {
                "name": "Podstawy wiersza poleceń Linuksa",
                "description": (
                    "Poczuj się pewnie w terminalu! Poruszaj się po systemie plików, zarządzaj plikami "
                    "i zrozum uprawnienia, czyli fundament bezpiecznych systemów."
                ),
            }
        },
        modules=[
            Module(
                title="First Steps in the Terminal",
                translations={"pl": {"title": "Pierwsze kroki w terminalu"}},
                order_index=1,
                lessons=[
                    Lesson(
                        title="Navigating the File System",
                        translations={"pl": {"title": "Poruszanie się po systemie plików"}},
                        xp_reward=10,
                        exercises=[
                            Exercise(
                                type=ExerciseType.multiple_choice,
                                content="What does the pwd command show?",
                                translations={
                                    "pl": {
                                        "content": "Co pokazuje polecenie pwd?",
                                        "correct_answer": "Bieżący katalog",
                                        "options": [
                                            "Bieżący katalog",
                                            "Listę plików",
                                            "Hasło użytkownika",
                                            "Uruchomione procesy",
                                        ],
                                    }
                                },
                                correct_answer="The current directory",
                                options=[
                                    "The current directory",
                                    "A list of files",
                                    "The user's password",
                                    "Running processes",
                                ],
                            ),
                            Exercise(
                                type=ExerciseType.block_assembly,
                                content="Go to the directory /home/student.",
                                translations={"pl": {"content": "Przejdź do katalogu /home/student."}},
                                correct_answer="cd /home/student",
                                options=["cd", "/home/student", "ls", "mv", "goto"],
                            ),
                            Exercise(
                                type=ExerciseType.matching,
                                content="Match each command with what it does.",
                                translations={
                                    "pl": {
                                        "content": "Dopasuj każde polecenie do tego, co robi.",
                                        "correct_answer": (
                                            "pwd: pokazuje bieżący katalog; ls: wyświetla pliki; "
                                            "cd: zmienia katalog; mkdir: tworzy katalog"
                                        ),
                                        "options": [
                                            ["pwd", "Pokazuje bieżący katalog"],
                                            ["ls", "Wyświetla pliki"],
                                            ["cd", "Zmienia katalog"],
                                            ["mkdir", "Tworzy katalog"],
                                        ],
                                    }
                                },
                                correct_answer=(
                                    "pwd: shows the current directory; ls: lists files; "
                                    "cd: changes directory; mkdir: creates a directory"
                                ),
                                options=[
                                    ["pwd", "Shows the current directory"],
                                    ["ls", "Lists files"],
                                    ["cd", "Changes directory"],
                                    ["mkdir", "Creates a directory"],
                                ],
                            ),
                        ],
                    ),
                    Lesson(
                        title="Working with Files",
                        translations={"pl": {"title": "Praca z plikami"}},
                        xp_reward=10,
                        exercises=[
                            Exercise(
                                type=ExerciseType.code,
                                content='Print the text "Hello Linux" in the terminal.',
                                translations={"pl": {"content": 'Wypisz w terminalu tekst "Hello Linux".'}},
                                code_snippet='echo "Hello Linux"',
                                correct_answer="Hello Linux",
                            ),
                            Exercise(
                                type=ExerciseType.multiple_choice,
                                content="Which command copies a file?",
                                translations={"pl": {"content": "Które polecenie kopiuje plik?"}},
                                correct_answer="cp",
                                options=["cp", "mv", "rm", "cat"],
                            ),
                            Exercise(
                                type=ExerciseType.block_assembly,
                                content="Copy the file notes.txt to a new file backup.txt.",
                                translations={"pl": {"content": "Skopiuj plik notes.txt do nowego pliku backup.txt."}},
                                correct_answer="cp notes.txt backup.txt",
                                options=["cp", "notes.txt", "backup.txt", "mv", "rm", ">"],
                            ),
                            Exercise(
                                type=ExerciseType.code,
                                content="Create a new directory named projects.",
                                translations={"pl": {"content": "Utwórz nowy katalog o nazwie projects."}},
                                code_snippet="mkdir projects",
                                correct_answer="A new directory named projects is created (no output).",
                            ),
                        ],
                    ),
                    Lesson(
                        title="Permissions and Security",
                        translations={"pl": {"title": "Uprawnienia i bezpieczeństwo"}},
                        xp_reward=10,
                        exercises=[
                            Exercise(
                                type=ExerciseType.multiple_choice,
                                content="What does the chmod command change?",
                                translations={
                                    "pl": {
                                        "content": "Co zmienia polecenie chmod?",
                                        "correct_answer": "Uprawnienia pliku",
                                        "options": [
                                            "Uprawnienia pliku",
                                            "Nazwę pliku",
                                            "Właściciela komputera",
                                            "Zawartość pliku",
                                        ],
                                    }
                                },
                                correct_answer="A file's permissions",
                                options=[
                                    "A file's permissions",
                                    "A file's name",
                                    "The computer's owner",
                                    "A file's contents",
                                ],
                            ),
                            Exercise(
                                type=ExerciseType.matching,
                                content="Match each permission letter with its meaning.",
                                translations={
                                    "pl": {
                                        "content": "Dopasuj każdą literę uprawnień do jej znaczenia.",
                                        "correct_answer": "r: odczyt; w: zapis; x: wykonanie",
                                        "options": [["r", "Odczyt"], ["w", "Zapis"], ["x", "Wykonanie"]],
                                    }
                                },
                                correct_answer="r: read; w: write; x: execute",
                                options=[["r", "Read"], ["w", "Write"], ["x", "Execute"]],
                            ),
                            Exercise(
                                type=ExerciseType.code,
                                content="Make the file script.sh executable.",
                                translations={"pl": {"content": "Nadaj plikowi script.sh prawo do wykonywania."}},
                                code_snippet="chmod +x script.sh",
                                correct_answer="script.sh becomes executable (no output).",
                            ),
                            Exercise(
                                type=ExerciseType.multiple_choice,
                                content="What does putting sudo before a command do?",
                                translations={
                                    "pl": {
                                        "content": "Co robi sudo dopisane przed poleceniem?",
                                        "correct_answer": "Uruchamia polecenie z uprawnieniami administratora",
                                        "options": [
                                            "Uruchamia polecenie z uprawnieniami administratora",
                                            "Uruchamia polecenie szybciej",
                                            "Cofa ostatnie polecenie",
                                            "Wyłącza komputer",
                                        ],
                                    }
                                },
                                correct_answer="Runs the command with administrator rights",
                                options=[
                                    "Runs the command with administrator rights",
                                    "Runs the command faster",
                                    "Undoes the last command",
                                    "Shuts down the computer",
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            quiz_module(
                2,
                [
                    Exercise(
                        type=ExerciseType.multiple_choice,
                        content="Which command lists the files in the current directory?",
                        translations={"pl": {"content": "Które polecenie wyświetla pliki w bieżącym katalogu?"}},
                        correct_answer="ls",
                        options=["ls", "pwd", "cd", "echo"],
                    ),
                    Exercise(
                        type=ExerciseType.multiple_choice,
                        content="Which command moves or renames a file?",
                        translations={"pl": {"content": "Które polecenie przenosi plik lub zmienia jego nazwę?"}},
                        correct_answer="mv",
                        options=["mv", "cp", "rm", "mkdir"],
                    ),
                    Exercise(
                        type=ExerciseType.multiple_choice,
                        content="What does cd .. do?",
                        translations={
                            "pl": {
                                "content": "Co robi cd ..?",
                                "correct_answer": "Przechodzi do katalogu nadrzędnego",
                                "options": [
                                    "Przechodzi do katalogu nadrzędnego",
                                    "Usuwa bieżący katalog",
                                    "Przechodzi do katalogu domowego",
                                    "Wyświetla ukryte pliki",
                                ],
                            }
                        },
                        correct_answer="Moves to the parent directory",
                        options=[
                            "Moves to the parent directory",
                            "Deletes the current directory",
                            "Moves to the home directory",
                            "Shows hidden files",
                        ],
                    ),
                    Exercise(
                        type=ExerciseType.multiple_choice,
                        content="Which permission letter allows running a file as a program?",
                        translations={"pl": {"content": "Która litera uprawnień pozwala uruchomić plik jako program?"}},
                        correct_answer="x",
                        options=["x", "r", "w", "s"],
                    ),
                    Exercise(
                        type=ExerciseType.chat,
                        content="Why shouldn't you use sudo or the root account for everyday work?",
                        translations={
                            "pl": {"content": "Dlaczego nie warto używać sudo ani konta root do codziennej pracy?"}
                        },
                        correct_answer=(
                            "With administrator rights a typo or a malicious program can change or delete "
                            "anything in the system; working as a normal user limits the damage to your own "
                            "files, so you use sudo only for the commands that really need it."
                        ),
                    ),
                ],
            ),
        ],
    )


# =============================================================================
# Backend Engineering: Java Basics
# =============================================================================
def java_course() -> Course:
    return Course(
        name="Java Basics",
        description=(
            "Write your first lines of Java, the language behind countless backend systems. "
            "Learn variables, conditions and methods step by step."
        ),
        icon_url="https://raw.githubusercontent.com/github/explore/main/topics/java/java.png",
        language="java",
        track=Track.backend,
        xp_reward=150,
        translations={
            "pl": {
                "name": "Podstawy Javy",
                "description": (
                    "Napisz pierwsze linijki w Javie, języku, na którym działa mnóstwo systemów backendowych. "
                    "Poznaj zmienne, warunki i metody krok po kroku."
                ),
            }
        },
        modules=[
            Module(
                title="First Steps in Java",
                translations={"pl": {"title": "Pierwsze kroki w Javie"}},
                order_index=1,
                lessons=[
                    Lesson(
                        title="Printing and Variables",
                        translations={"pl": {"title": "Wypisywanie i zmienne"}},
                        xp_reward=10,
                        exercises=[
                            Exercise(
                                type=ExerciseType.block_assembly,
                                content='Display the text "Hello Java" on the screen.',
                                translations={"pl": {"content": 'Wyświetl na ekranie tekst "Hello Java".'}},
                                correct_answer='System.out.println ( "Hello Java" ) ;',
                                options=["System.out.println", "(", '"Hello Java"', ")", ";", "print", "echo", ":"],
                            ),
                            Exercise(
                                type=ExerciseType.multiple_choice,
                                content="Which type stores whole numbers in Java?",
                                translations={"pl": {"content": "Który typ przechowuje liczby całkowite w Javie?"}},
                                correct_answer="int",
                                options=["int", "String", "boolean", "double"],
                            ),
                            Exercise(
                                type=ExerciseType.code,
                                content='Print "Hello, Backend!" to the console.',
                                translations={"pl": {"content": 'Wypisz w konsoli "Hello, Backend!".'}},
                                code_snippet='System.out.println("Hello, Backend!");',
                                correct_answer="Hello, Backend!",
                            ),
                        ],
                    ),
                    Lesson(
                        title="Conditions",
                        translations={"pl": {"title": "Warunki"}},
                        xp_reward=10,
                        exercises=[
                            Exercise(
                                type=ExerciseType.matching,
                                content="Match each type with the kind of value it stores.",
                                translations={
                                    "pl": {
                                        "content": "Dopasuj każdy typ do rodzaju wartości, jaką przechowuje.",
                                        "correct_answer": (
                                            "int: liczba całkowita; double: liczba dziesiętna; "
                                            "boolean: prawda lub fałsz; String: tekst"
                                        ),
                                        "options": [
                                            ["int", "Liczba całkowita"],
                                            ["double", "Liczba dziesiętna"],
                                            ["boolean", "Prawda lub fałsz"],
                                            ["String", "Tekst"],
                                        ],
                                    }
                                },
                                correct_answer=(
                                    "int: whole number; double: decimal number; "
                                    "boolean: true or false; String: text"
                                ),
                                options=[
                                    ["int", "Whole number"],
                                    ["double", "Decimal number"],
                                    ["boolean", "True or false"],
                                    ["String", "Text"],
                                ],
                            ),
                            Exercise(
                                type=ExerciseType.multiple_choice,
                                content="Which operator checks whether two numbers are equal?",
                                translations={"pl": {"content": "Który operator sprawdza, czy dwie liczby są równe?"}},
                                correct_answer="==",
                                options=["==", "=", "!=", "=>"],
                            ),
                            Exercise(
                                type=ExerciseType.code,
                                content=(
                                    "Create an int variable age with the value 20. "
                                    'If age is at least 18, print "Adult".'
                                ),
                                translations={
                                    "pl": {
                                        "content": (
                                            "Utwórz zmienną typu int o nazwie age i wartości 20. "
                                            'Jeśli age wynosi co najmniej 18, wypisz "Adult".'
                                        )
                                    }
                                },
                                code_snippet='int age = 20;\nif (age >= 18) {\n    System.out.println("Adult");\n}',
                                correct_answer="Adult",
                            ),
                        ],
                    ),
                    Lesson(
                        title="Methods",
                        translations={"pl": {"title": "Metody"}},
                        xp_reward=10,
                        exercises=[
                            Exercise(
                                type=ExerciseType.multiple_choice,
                                content="What does void mean in a method declaration?",
                                translations={
                                    "pl": {
                                        "content": "Co oznacza void w deklaracji metody?",
                                        "correct_answer": "Metoda nic nie zwraca",
                                        "options": [
                                            "Metoda nic nie zwraca",
                                            "Metoda jest pusta",
                                            "Metoda zwraca liczbę",
                                            "Metoda jest prywatna",
                                        ],
                                    }
                                },
                                correct_answer="The method returns nothing",
                                options=[
                                    "The method returns nothing",
                                    "The method is empty",
                                    "The method returns a number",
                                    "The method is private",
                                ],
                            ),
                            Exercise(
                                type=ExerciseType.block_assembly,
                                content="Start the declaration of a method add that takes two ints and returns an int.",
                                translations={
                                    "pl": {
                                        "content": "Rozpocznij deklarację metody add, która przyjmuje dwa inty i zwraca int."
                                    }
                                },
                                correct_answer="static int add ( int a , int b )",
                                options=["static", "int", "add", "(", "int", "a", ",", "int", "b", ")", "void", "def"],
                            ),
                            Exercise(
                                type=ExerciseType.code,
                                content="Write a method square that takes an int x and returns x multiplied by itself.",
                                translations={
                                    "pl": {
                                        "content": "Napisz metodę square, która przyjmuje int x i zwraca x pomnożone przez siebie."
                                    }
                                },
                                code_snippet="static int square(int x) {\n    return x * x;\n}",
                                correct_answer="square(4) returns 16",
                            ),
                        ],
                    ),
                ],
            ),
            quiz_module(
                2,
                [
                    Exercise(
                        type=ExerciseType.multiple_choice,
                        content="Which line prints text in Java?",
                        translations={"pl": {"content": "Która linia wypisuje tekst w Javie?"}},
                        correct_answer='System.out.println("Hi");',
                        options=['System.out.println("Hi");', 'print("Hi")', 'echo "Hi"', 'console.log("Hi");'],
                    ),
                    Exercise(
                        type=ExerciseType.multiple_choice,
                        content="Which type would you use to store the value true?",
                        translations={"pl": {"content": "Jakiego typu użyjesz do przechowania wartości true?"}},
                        correct_answer="boolean",
                        options=["boolean", "int", "String", "double"],
                    ),
                    Exercise(
                        type=ExerciseType.multiple_choice,
                        content="What does every Java statement end with?",
                        translations={"pl": {"content": "Czym kończy się każda instrukcja w Javie?"}},
                        correct_answer=";",
                        options=[";", ":", ".", "}"],
                    ),
                    Exercise(
                        type=ExerciseType.multiple_choice,
                        content="What does square(3) return if the method returns x * x?",
                        translations={"pl": {"content": "Co zwróci square(3), jeśli metoda zwraca x * x?"}},
                        correct_answer="9",
                        options=["9", "6", "3", "33"],
                    ),
                    Exercise(
                        type=ExerciseType.chat,
                        content="Why does Java make you declare the type of every variable?",
                        translations={
                            "pl": {"content": "Dlaczego Java wymaga deklarowania typu każdej zmiennej?"}
                        },
                        correct_answer=(
                            "Declared types let the compiler catch mistakes, like putting text into a number "
                            "variable, before the program runs, and make the code clearer to read, which "
                            "matters in large backend systems."
                        ),
                    ),
                ],
            ),
        ],
    )


TRACK_COURSES = [data_analysis_course, linux_course, java_course]


def seed_track_courses(db: Session, force: bool = False) -> None:
    """Add the sample area courses that are missing; with force, recreate them."""
    for build in TRACK_COURSES:
        course = build()
        existing = db.query(Course).filter(Course.name == course.name).first()
        if existing and not force:
            print(f"Course '{course.name}' already exists. Skipping.")
            continue
        if existing:
            db.delete(existing)
            db.flush()
        print(f"Seeding area course: '{course.name}'...")
        db.add(course)
    db.commit()
