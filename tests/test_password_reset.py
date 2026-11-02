import re

import pytest

from src.api import auth
from src.core.security import hash_password

LINK = re.compile(r"http://localhost:5173/reset-password\?token=(\S+)")


@pytest.fixture
def sent(monkeypatch):
    """Emails the app would send, as (to, subject, body)."""
    outbox = []
    monkeypatch.setattr(auth, "send_email", lambda *email: outbox.append(email))
    return outbox


@pytest.fixture
def user(make_user):
    return make_user(password=hash_password("secret123"))


def forgot(client, email="probe@example.com", language="en"):
    return client.post(
        "/api/auth/forgot-password", json={"email": email}, headers={"Accept-Language": language}
    )


def reset(client, token, password="newpass1"):
    return client.post("/api/auth/reset-password", json={"token": token, "password": password})


def login(client, password):
    return client.post(
        "/api/auth/login", json={"username_or_email": "probe", "password": password}
    )


def token_from(email):
    return LINK.search(email[2]).group(1)


def test_forgot_password_emails_a_link_in_the_ui_language(client, user, sent):
    assert forgot(client, language="pl").status_code == 204
    assert len(sent) == 1
    to, subject, body = sent[0]
    assert to == "probe@example.com"
    assert "hasło" in subject
    assert LINK.search(body)


def test_forgot_password_answers_the_same_for_an_unknown_email(client, user, sent):
    assert forgot(client, email="nobody@example.com").status_code == 204
    assert sent == []


def test_reset_sets_the_new_password(client, user, sent):
    forgot(client)
    assert reset(client, token_from(sent[0])).status_code == 204
    assert login(client, "newpass1").status_code == 200
    assert login(client, "secret123").status_code == 401


def test_reset_link_works_only_once(client, user, sent):
    forgot(client)
    token = token_from(sent[0])
    reset(client, token)
    response = reset(client, token, password="another1")
    assert response.status_code == 400


def test_reset_rejects_a_forged_token(client, user):
    assert reset(client, "not-a-token").status_code == 400


def test_reset_token_is_not_an_access_token(client, user, sent):
    forgot(client)
    headers = {"Authorization": f"Bearer {token_from(sent[0])}"}
    assert client.get("/api/auth/me", headers=headers).status_code == 401


def test_reset_validates_the_new_password(client, user, sent):
    forgot(client)
    assert reset(client, token_from(sent[0]), password="short").status_code == 422
