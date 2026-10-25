from types import SimpleNamespace as NS

from src.core.profile import next_lesson, suggest_course
from src.crud.profile import _localized_title


def course(cid, track, modules=()):
    return NS(id=cid, track=track, modules=list(modules))


def module(order, lesson_ids):
    return NS(
        order_index=order,
        title=f"M{order}",
        lessons=[NS(id=i, title=f"L{i}") for i in lesson_ids],
    )


def test_next_lesson_follows_module_order():
    c = course(1, None, [module(2, [30]), module(1, [10, 11])])
    mod, les = next_lesson(c, {10})
    assert (mod.order_index, les.id) == (1, 11)


def test_next_lesson_none_when_done():
    assert next_lesson(course(1, None, [module(1, [10])]), {10}) is None


def test_suggest_prefers_track():
    cs = [course(1, "data_science"), course(2, "backend"), course(3, "backend")]
    assert suggest_course(cs, {2}, "backend").id == 3


def test_suggest_falls_back_to_any_area():
    cs = [course(1, "data_science"), course(2, "backend")]
    assert suggest_course(cs, {2}, "backend").id == 1


def test_suggest_none_when_all_started():
    assert suggest_course([course(1, "linux")], {1}, "linux") is None


def test_suggest_without_area_takes_first_fresh_course():
    # No area chosen: a course without an area must not be preferred.
    cs = [course(1, "linux"), course(2, None)]
    assert suggest_course(cs, set(), None).id == 1


def test_localized_title_falls_back_on_empty_translation():
    item = NS(title="Loops", translations={"pl": {"title": ""}})
    assert _localized_title(item, "pl") == "Loops"
