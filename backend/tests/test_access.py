from unittest.mock import MagicMock

from app.access import check_access
from app.models import AccessEvent, Badge, Reader, User


def make_reader(active: bool = True) -> Reader:
    return Reader(
        id=1,
        reader_code="reader-lab-01",
        name="Lecteur RFID labo",
        api_key_hash="test-hash",
        active=active,
    )


def test_access_rejects_disabled_reader() -> None:
    db = MagicMock()
    reader = make_reader(active=False)

    result = check_access(
        db=db,
        reader=reader,
        raw_uid="26 35 58 12",
    )

    assert result.authorized is False
    assert result.reason == "reader_disabled"
    assert result.uid == "26355812"

    event = db.add.call_args.args[0]

    assert isinstance(event, AccessEvent)
    assert event.authorized is False
    assert event.reason == "reader_disabled"
    assert event.reader_id == 1

    db.commit.assert_called_once()


def test_access_rejects_disabled_badge() -> None:
    db = MagicMock()
    reader = make_reader()

    badge = Badge(
        id=1,
        uid="26355812",
        user_id=1,
        label="Badge test",
        active=False,
    )

    user = User(
        id=1,
        full_name="Karim Assouli",
        active=True,
    )

    db.scalar.return_value = badge
    db.get.return_value = user

    result = check_access(
        db=db,
        reader=reader,
        raw_uid="26 35 58 12",
    )

    assert result.authorized is False
    assert result.reason == "badge_disabled"
    assert result.uid == "26355812"
    assert result.user_id == 1

    event = db.add.call_args.args[0]

    assert isinstance(event, AccessEvent)
    assert event.authorized is False
    assert event.reason == "badge_disabled"
    assert event.badge_id == 1
    assert event.user_id == 1

    db.commit.assert_called_once()


def test_access_rejects_disabled_user() -> None:
    db = MagicMock()
    reader = make_reader()

    badge = Badge(
        id=1,
        uid="26355812",
        user_id=1,
        label="Badge test",
        active=True,
    )

    user = User(
        id=1,
        full_name="Karim Assouli",
        active=False,
    )

    db.scalar.return_value = badge
    db.get.return_value = user

    result = check_access(
        db=db,
        reader=reader,
        raw_uid="26 35 58 12",
    )

    assert result.authorized is False
    assert result.reason == "user_disabled"
    assert result.uid == "26355812"
    assert result.user_id == 1

    event = db.add.call_args.args[0]

    assert isinstance(event, AccessEvent)
    assert event.authorized is False
    assert event.reason == "user_disabled"
    assert event.badge_id == 1
    assert event.user_id == 1

    db.commit.assert_called_once()
