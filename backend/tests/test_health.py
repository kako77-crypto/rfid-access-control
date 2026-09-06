from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_when_database_is_available(monkeypatch) -> None:
    monkeypatch.setattr("app.main.database_is_ready", lambda: True)

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_ready_when_database_is_unavailable(monkeypatch) -> None:
    monkeypatch.setattr("app.main.database_is_ready", lambda: False)

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {"status": "not ready"}

