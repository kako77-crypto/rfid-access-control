from fastapi import Depends, FastAPI, Header, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.access import check_access
from app.database import database_is_ready, get_db
from app.models import Reader
from app.schemas import AccessCheckRequest, AccessCheckResponse
from app.security import verify_api_key

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


@app.post("/api/v1/access/check", response_model=AccessCheckResponse)
def access_check(
    request: AccessCheckRequest,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    db: Session = Depends(get_db),
) -> AccessCheckResponse:
    """Evaluate one RFID badge against a configured reader."""
    reader = db.scalar(
        select(Reader).where(Reader.reader_code == request.reader_code)
    )

    if reader is None or x_api_key is None or not verify_api_key(x_api_key, reader.api_key_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid reader credentials",
        )

    try:
        return check_access(
            db=db,
            reader=reader,
            raw_uid=request.uid,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
