from sqlalchemy import create_engine, text

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def database_is_ready() -> bool:
    """Return whether a connection can be established and queried."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:  # Readiness deliberately converts connection errors to a status.
        return False
    return True

