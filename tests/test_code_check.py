import ast
import textwrap

from src.core.code_check import constructs, passes_python_checks

LOOP = "i = 1\nwhile i <= 3:\n    print(i)\n    i += 1"
BRANCH = 'score = 75\nif score >= 50:\n    print("Pass")\nelse:\n    print("Retake")'


def test_constructs_finds_loops_branches_and_containers():
    tree = ast.parse("def f(x):\n    for y in [1]:\n        return {}\n" + BRANCH)
    assert constructs(tree) == {"def", "for", "return", "list", "dict", "if", "else"}


def test_else_only_counts_when_present():
    assert "else" not in constructs(ast.parse("if x:\n    pass"))


def test_answer_with_other_names_passes():
    assert passes_python_checks("n = 1\nwhile n < 4:\n    print(n)\n    n = n + 1", LOOP)


def test_syntax_error_fails():
    assert not passes_python_checks("while i <= 3\n    print(i)", LOOP)


def test_missing_construct_fails():
    # Correct output, but the task asks for a while loop.
    assert not passes_python_checks("for i in range(1, 4):\n    print(i)", LOOP)
    assert not passes_python_checks('if 75 >= 50:\n    print("Pass")', BRANCH)


def test_extra_constructs_are_allowed():
    wrapped = "def show():\n" + textwrap.indent(LOOP, "    ") + "\nshow()"
    assert passes_python_checks(wrapped, LOOP)
