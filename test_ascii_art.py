from ascii_art import make_smile


def test_make_smile():
    assert make_smile() == ":)"


def test_make_smile_returns_string():
    assert isinstance(make_smile(), str)


def test_make_smile_is_not_empty():
    assert make_smile() != ""
