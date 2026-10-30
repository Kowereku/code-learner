from tests.conftest import auth_headers

PL = {"Accept-Language": "pl-PL,pl;q=0.9"}
NEW_COURSE = {"name": "New course", "language": "python"}


def listed(client, course_id, headers=None):
    courses = client.get("/api/courses", headers=headers or {}).json()
    return next(course for course in courses if course["id"] == course_id)


def test_course_list_counts_modules_and_lessons(client, course_tree):
    course = listed(client, course_tree.course.id)
    assert (course["name"], course["modules_count"], course["lessons_count"]) == ("Test course", 2, 2)


def test_course_list_is_translated(client, course_tree):
    assert listed(client, course_tree.course.id, PL)["name"] == "Kurs testowy"


def test_course_detail_lists_modules_in_order(client, course_tree):
    body = client.get(f"/api/courses/{course_tree.course.id}").json()
    assert body["language"] == "python"
    assert [module["title"] for module in body["modules"]] == ["Basics", "Quiz"]
    assert [lesson["title"] for lesson in body["modules"][0]["lessons"]] == ["Loops"]


def test_unknown_course_lesson_and_exercise_are_404(client):
    for url in ("/api/courses/0", "/api/lessons/0", "/api/exercises/0"):
        assert client.get(url).status_code == 404


def test_lesson_detail_has_its_exercises_and_translation(client, course_tree):
    body = client.get(f"/api/lessons/{course_tree.lesson.id}", headers=PL).json()
    assert body["title"] == "Pętle"
    assert [exercise["id"] for exercise in body["exercises"]] == [course_tree.code.id]
    assert body["exercises"][0]["code_snippet"] == course_tree.code.code_snippet


def test_creating_a_course_needs_a_login(client, make_user):
    assert client.post("/api/courses", json=NEW_COURSE).status_code == 401
    response = client.post("/api/courses", json=NEW_COURSE, headers=auth_headers(make_user()))
    assert response.status_code == 201
    assert (response.json()["name"], response.json()["lessons_count"]) == ("New course", 0)


def test_untranslated_locale_falls_back_to_english(client, course_tree):
    body = client.get(f"/api/lessons/{course_tree.lesson.id}", headers={"Accept-Language": "de"})
    assert body.json()["title"] == "Loops"
