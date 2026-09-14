from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app
from app.models import Reader
from app.security import hash_api_key


def override_db():
    db = MagicMock()
    yield db


app.dependency_overrides[get_db] = override_db
client = TestClient(app)


def test_access_check_rejects_missing_api_key() -> None:
    response = client.post(
        "/api/v1/access/check",
        json={
            "reader_code": "reader-lab-01",
            "uid": "26 35 58 12",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid reader credentials"}


def test_access_check_rejects_wrong_api_key(monkeypatch) -> None:
    reader = Reader(
        id=1,
        reader_code="reader-lab-01",
        name="Lecteur RFID labo",
        api_key_hash=hash_api_key("correct-key"),
        active=True,
    )

    db = MagicMock()
    db.scalar.return_value = reader

    def override():
        yield db

    app.dependency_overrides[get_db] = override

    response = client.post(
        "/api/v1/access/check",
        headers={"X-API-Key": "wrong-key"},
        json={
            "reader_code": "reader-lab-01",
            "uid": "26 35 58 12",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid reader credentials"}


def test_access_check_accepts_valid_api_key(monkeypatch) -> None:
    reader = Reader(
        id=1,
        reader_code="reader-lab-01",
        name="Lecteur RFID labo",
        api_key_hash=hash_api_key("correct-key"),
        active=True,
    )

    db = MagicMock()
    db.scalar.return_value = reader

    def override():
        yield db

    app.dependency_overrides[get_db] = override

    monkeypatch.setattr(
        "app.main.check_access",
        lambda db, reader, raw_uid: {
            "authorized": True,
            "reason": "authorized",
            "uid": "26355812",
            "user_id": 1,
            "user_name": "Karim Assouli",
        },
    )

    response = client.post(
        "/api/v1/access/check",
        headers={"X-API-Key": "correct-key"},
        json={
            "reader_code": "reader-lab-01",
            "uid": "26 35 58 12",
        },
    )

    assert response.status_code == 200
    assert response.json()["authorized"] is True
    assert response.json()["uid"] == "26355812"
