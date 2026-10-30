import logging

from fastapi import HTTPException
from fastapi.testclient import TestClient

from src.core import ai
from src.main import app

FRONTEND = {"Origin": "http://localhost:5173"}


def _boom():
    raise RuntimeError("kaboom")


def _not_found():
    raise HTTPException(status_code=404, detail="Nope")


def _ducky_unavailable():
    raise HTTPException(status_code=503, detail="Ducky is unavailable right now. Try again in a moment.")


# Test-only routes: one that crashes unexpectedly, two that raise normal HTTP errors.
app.add_api_route("/__test__/boom", _boom)
app.add_api_route("/__test__/not-found", _not_found)
app.add_api_route("/__test__/ducky", _ducky_unavailable)
# raise_server_exceptions stays on: a crash that isn't caught by the app fails the test.
client = TestClient(app)


def test_unexpected_error_returns_json_500(caplog):
    with caplog.at_level(logging.ERROR):
        response = client.get("/__test__/boom", headers=FRONTEND)
    assert response.status_code == 500
    assert response.json() == {"detail": "Something went wrong on our side."}
    assert "kaboom" in caplog.text


def test_unexpected_error_keeps_cors_headers():
    # Without them the browser hides the response and reports a network error instead.
    response = client.get("/__test__/boom", headers=FRONTEND)
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_http_errors_are_unchanged():
    response = client.get("/__test__/not-found", headers=FRONTEND)
    assert (response.status_code, response.json()) == (404, {"detail": "Nope"})
    response = client.get("/__test__/ducky", headers=FRONTEND)
    assert response.status_code == 503
    assert response.json()["detail"].startswith("Ducky is unavailable")


def test_ai_timeout_is_sixty_seconds():
    assert ai.AI_TIMEOUT_SECONDS == 60
