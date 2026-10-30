from src.model.user_lesson import UserLesson
from tests.conftest import auth_headers


def complete(client, user, lesson, mistakes=0):
    return client.post(
        f"/api/lessons/{lesson.id}/complete",
        json={"mistakes_made": mistakes},
        headers=auth_headers(user),
    )


def test_first_completion_awards_lesson_xp(client, make_user, course_tree):
    user = make_user()
    body = complete(client, user, course_tree.lesson, mistakes=2).json()
    assert (body["is_first_completion"], body["xp_earned"], body["total_xp"]) == (True, 10, 10)
    assert body["mistakes_made"] == 2
    assert body["course_completed"] is None


def test_replay_awards_no_xp(client, make_user, course_tree):
    user = make_user()
    complete(client, user, course_tree.lesson)
    body = complete(client, user, course_tree.lesson).json()
    assert (body["is_first_completion"], body["xp_earned"], body["total_xp"]) == (False, 0, 10)


def test_replay_keeps_the_best_mistake_count(client, db, make_user, course_tree):
    user = make_user()
    complete(client, user, course_tree.lesson, mistakes=3)
    assert complete(client, user, course_tree.lesson, mistakes=1).json()["mistakes_made"] == 1
    assert complete(client, user, course_tree.lesson, mistakes=4).json()["mistakes_made"] == 1
    assert db.get(UserLesson, (user.id, course_tree.lesson.id)).mistakes_made == 1


def test_last_lesson_awards_the_course_bonus_once(client, make_user, course_tree):
    user = make_user()
    complete(client, user, course_tree.lesson)
    last = complete(client, user, course_tree.quiz).json()
    assert last["course_completed"] == {
        "course_id": course_tree.course.id,
        "course_name": "Test course",
        "bonus_xp": 50,
    }
    assert (last["xp_earned"], last["total_xp"]) == (20 + 50, 10 + 20 + 50)

    replay = complete(client, user, course_tree.quiz).json()
    assert (replay["course_completed"], replay["xp_earned"], replay["total_xp"]) == (None, 0, 80)


def test_complete_needs_a_known_lesson_and_a_login(client, make_user, course_tree):
    user = make_user()
    missing = client.post("/api/lessons/0/complete", json={}, headers=auth_headers(user))
    assert missing.status_code == 404
    anonymous = client.post(f"/api/lessons/{course_tree.lesson.id}/complete", json={})
    assert anonymous.status_code == 401


def test_complete_rejects_negative_mistakes(client, make_user, course_tree):
    assert complete(client, make_user(), course_tree.lesson, mistakes=-1).status_code == 422


def test_progress_lists_completed_lessons_with_their_course(client, make_user, course_tree):
    user = make_user()
    complete(client, user, course_tree.lesson)
    response = client.get("/api/progress", headers=auth_headers(user))
    assert response.json() == {
        "completed_lessons": [
            {"lesson_id": course_tree.lesson.id, "course_id": course_tree.course.id}
        ]
    }


def test_lesson_progress_is_saved_and_read_back(client, make_user, course_tree):
    user = make_user()
    url = f"/api/progress/users/me/lessons/{course_tree.lesson.id}/progress"
    assert client.get(url, headers=auth_headers(user)).status_code == 404

    saved = client.put(
        url, json={"status": "in_progress", "last_position": 1}, headers=auth_headers(user)
    )
    assert saved.status_code == 200
    body = client.get(url, headers=auth_headers(user)).json()
    assert (body["status"], body["last_position"]) == ("in_progress", 1)


def test_lesson_progress_needs_a_known_lesson(client, make_user):
    url = "/api/progress/users/me/lessons/0/progress"
    assert client.put(url, json={}, headers=auth_headers(make_user())).status_code == 404
