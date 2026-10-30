from src.core.security import verify_password
from src.model.user import User
from tests.conftest import auth_headers

NEW_USER = {"username": "probe_new", "email": "probe_new@example.com", "password": "secret123"}


def register(client, **fields):
    return client.post("/api/auth/register", json=NEW_USER | fields)


def test_register_creates_user_with_hashed_password(client, db):
    response = register(client)
    assert response.status_code == 201
    body = response.json()
    assert (body["username"], body["email"], body["total_xp"]) == ("probe_new", "probe_new@example.com", 0)
    assert "password" not in body
    stored = db.get(User, body["id"]).password
    assert stored != "secret123" and verify_password("secret123", stored)


def test_register_rejects_taken_username(client):
    register(client)
    response = register(client, email="other@example.com")
    assert (response.status_code, response.json()["detail"]) == (400, "Username is already taken.")


def test_register_rejects_taken_email(client):
    register(client)
    response = register(client, username="probe_other")
    assert (response.status_code, response.json()["detail"]) == (400, "Email is already registered.")


def test_register_validates_input(client):
    assert register(client, email="not-an-email").status_code == 422
    assert register(client, password="short").status_code == 422


def test_login_with_username_or_email_returns_a_working_token(client):
    register(client)
    for identifier in ("probe_new", "probe_new@example.com"):
        response = client.post(
            "/api/auth/login", json={"username_or_email": identifier, "password": "secret123"}
        )
        assert response.status_code == 200
        token = response.json()["access_token"]
        me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me.json()["username"] == "probe_new"


def test_login_rejects_wrong_password_and_unknown_user(client):
    register(client)
    for identifier, password in (("probe_new", "wrong-pass"), ("nobody_here", "secret123")):
        response = client.post(
            "/api/auth/login", json={"username_or_email": identifier, "password": password}
        )
        # The same answer for both, so the login form doesn't reveal which accounts exist.
        assert (response.status_code, response.json()["detail"]) == (
            401,
            "Wrong email/username or password",
        )


def test_me_returns_the_logged_in_user(client, make_user):
    user = make_user(total_xp=120)
    response = client.get("/api/auth/me", headers=auth_headers(user))
    assert response.status_code == 200
    assert (response.json()["id"], response.json()["total_xp"]) == (user.id, 120)


def test_me_rejects_missing_broken_and_orphaned_tokens(client, db, make_user):
    user = make_user()
    orphaned = auth_headers(user)
    db.delete(user)
    db.flush()
    for headers in ({}, {"Authorization": "Bearer not-a-jwt"}, orphaned):
        assert client.get("/api/auth/me", headers=headers).status_code == 401
