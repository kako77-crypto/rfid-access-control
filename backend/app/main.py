from fastapi import FastAPI, Response, status

from app.database import database_is_ready

app = FastAPI(title="RFID Access Control API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Report that the API process is running."""
    return {"status": "ok"}


@app.get("/ready")
def ready(response: Response) -> dict[str, str]:
    """Report whether the API can reach its required database dependency."""
    if not database_is_ready():
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not ready"}
    return {"status": "ready"}

