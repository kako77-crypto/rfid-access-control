import pytest

from app.rfid import normalize_uid


@pytest.mark.parametrize(
    ("raw_uid", "expected"),
    [
        ("26 35 58 12", "26355812"),
        ("26:35:58:12", "26355812"),
        ("26-35-58-12", "26355812"),
        ("26355812", "26355812"),
        ("26 35 58 12 ", "26355812"),
        ("c5 4a 54 73", "C54A5473"),
    ],
)
def test_normalize_uid(raw_uid: str, expected: str) -> None:
    assert normalize_uid(raw_uid) == expected


@pytest.mark.parametrize(
    "invalid_uid",
    [
        "",
        "   ",
        "26 35 ZZ 12",
        "2635581",
        "1234567890ABCDEF1234567890ABCDEF12",
    ],
)
def test_normalize_uid_rejects_invalid_values(invalid_uid: str) -> None:
    with pytest.raises(ValueError):
        normalize_uid(invalid_uid)
