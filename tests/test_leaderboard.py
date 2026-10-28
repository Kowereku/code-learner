from src.crud.leaderboard import get_leaderboard, rank_of

# Dev-database users have small XP, so these probes always rank above them.
BIG = 10**9


def test_ties_share_a_position(db, make_user):
    for name, xp in [("a", BIG + 300), ("b", BIG + 200), ("c", BIG + 200), ("d", BIG + 100)]:
        make_user(username=f"rank_{name}", email=f"rank_{name}@example.com", total_xp=xp)
    assert [rank_of(db, xp) for xp in (BIG + 300, BIG + 200, BIG + 100)] == [1, 2, 4]


def test_zero_xp_is_unranked(db, make_user):
    me = make_user(total_xp=0)
    assert rank_of(db, 0) is None
    assert get_leaderboard(db, me).me is None


def test_me_outside_the_top_ten(db, make_user):
    for i in range(11):
        make_user(username=f"top_{i}", email=f"top_{i}@example.com", total_xp=BIG + i)
    me = make_user(total_xp=5)
    board = get_leaderboard(db, me)
    assert len(board.top) == 10 and all(not row.is_me for row in board.top)
    assert board.me.is_me and board.me.position > 10


def test_me_inside_the_top_ten_is_flagged(db, make_user):
    me = make_user(total_xp=BIG * 2)
    board = get_leaderboard(db, me)
    assert board.top[0].is_me and board.top[0].position == 1
    assert board.me.position == 1 and board.me.level == board.top[0].level


def test_top_is_capped_at_ten_rows_when_users_tie(db, make_user):
    for i in range(12):
        make_user(username=f"tie_{i}", email=f"tie_{i}@example.com", total_xp=BIG * 3)
    me = make_user(total_xp=5)
    board = get_leaderboard(db, me)
    assert len(board.top) == 10
    assert {row.position for row in board.top} == {1}


def test_top_shows_tie_positions_and_skips_zero_xp(db, make_user):
    for name, xp in [("a", BIG + 300), ("b", BIG + 200), ("c", BIG + 200), ("d", BIG + 100)]:
        make_user(username=f"tp_{name}", email=f"tp_{name}@example.com", total_xp=xp)
    me = make_user(total_xp=0)
    board = get_leaderboard(db, me)
    assert [row.position for row in board.top[:4]] == [1, 2, 2, 4]
    assert [row.position for row in board.top[:4]] == [rank_of(db, row.total_xp) for row in board.top[:4]]
    assert all(row.total_xp > 0 for row in board.top)
