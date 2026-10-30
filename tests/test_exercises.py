from types import SimpleNamespace as NS

import httpx
import pytest

from src.core import ai
from tests.conftest import auth_headers

GOOD_LOOP = "n = 1\nwhile n <= 3:\n    print(n)\n    n += 1"


@pytest.fixture
def ducky(monkeypatch):
    """Stands in for the AI, so tests never call Ollama: records each call, returns `answer`."""
    fake = NS(calls=[], answer={"passed": True})

    def chat(messages, model):
        fake.calls.append(messages)
        if isinstance(fake.answer, Exception):
            raise fake.answer
        return fake.answer

    monkeypatch.setattr(ai, "chat", chat)
    return fake


def check(client, user, exercise, answer):
    return client.post(
        f"/api/exercises/{exercise.id}/check", json={"answer": answer}, headers=auth_headers(user)
    )


def ask(client, user, exercise, text="A list is mutable, a tuple is not.", locale="en"):
    return client.post(
        f"/api/exercises/{exercise.id}/chat",
        json={"messages": [{"role": "user", "content": text}], "locale": locale},
        headers=auth_headers(user),
    )


def test_check_fails_python_without_the_construct_and_skips_ducky(client, make_user, course_tree, ducky):
    response = check(client, make_user(), course_tree.code, "for i in range(1, 4):\n    print(i)")
    assert response.json() == {"passed": False}
    assert ducky.calls == []


@pytest.mark.parametrize("verdict", [True, False])
def test_check_returns_duckys_verdict(client, make_user, course_tree, ducky, verdict):
    ducky.answer = {"passed": verdict}
    response = check(client, make_user(), course_tree.code, GOOD_LOOP)
    assert response.json() == {"passed": verdict}
    system, student = ducky.calls[0]
    assert course_tree.code.code_snippet in system["content"]
    assert student == {"role": "user", "content": GOOD_LOOP}


def test_check_asks_ducky_directly_for_other_languages(client, db, make_user, course_tree, ducky):
    course_tree.course.language = "java"
    db.flush()
    assert check(client, make_user(), course_tree.code, "for (;;) {}").json() == {"passed": True}
    assert len(ducky.calls) == 1


@pytest.mark.parametrize(
    "failure",
    [httpx.ConnectError("Ollama is down"), {"verdict": "yes"}, {"passed": "maybe"}],
    ids=["unreachable", "missing key", "not a boolean"],
)
def test_check_ducky_failure_is_503(client, make_user, course_tree, ducky, failure):
    ducky.answer = failure
    response = check(client, make_user(), course_tree.code, GOOD_LOOP)
    assert response.status_code == 503
    assert response.json()["detail"].startswith("Ducky is unavailable")


def test_check_rejects_unknown_wrong_type_and_anonymous(client, make_user, course_tree, ducky):
    user = make_user()
    missing = client.post("/api/exercises/0/check", json={"answer": "x"}, headers=auth_headers(user))
    assert missing.status_code == 404
    assert check(client, user, course_tree.chat, GOOD_LOOP).status_code == 400
    anonymous = client.post(f"/api/exercises/{course_tree.code.id}/check", json={"answer": "x"})
    assert anonymous.status_code == 401
    assert ducky.calls == []


def test_chat_returns_duckys_reply(client, make_user, course_tree, ducky):
    ducky.answer = {"passed": True, "reply": "Exactly! Tuples are fixed."}
    response = ask(client, make_user(), course_tree.chat)
    assert response.json() == {"passed": True, "reply": "Exactly! Tuples are fixed."}
    system, student = ducky.calls[0]
    assert course_tree.chat.correct_answer in system["content"]
    # The outline lists what the course taught, without the quiz module.
    assert "The course covered: Basics (Loops)." in system["content"]
    assert student["content"] == "A list is mutable, a tuple is not."


def test_chat_replies_in_the_learners_language(client, make_user, course_tree, ducky):
    ducky.answer = {"passed": False, "reply": "Spróbuj jeszcze raz."}
    ask(client, make_user(), course_tree.chat, locale="pl")
    assert "written in Polish" in ducky.calls[0][0]["content"]


def test_chat_ducky_failure_is_503(client, make_user, course_tree, ducky):
    ducky.answer = {"passed": True, "reply": ""}
    assert ask(client, make_user(), course_tree.chat).status_code == 503


def test_chat_rejects_a_code_exercise(client, make_user, course_tree, ducky):
    assert ask(client, make_user(), course_tree.code).status_code == 400
    assert ducky.calls == []
