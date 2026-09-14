from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AccessEvent, Badge, Reader, User
from app.rfid import normalize_uid
from app.schemas import AccessCheckResponse


def check_access(
    db: Session,
    reader: Reader,
    raw_uid: str,
) -> AccessCheckResponse:
    """Evaluate one RFID access attempt and store the resulting event."""
    uid = normalize_uid(raw_uid)

    if not reader.active:
        return _record_result(
            db=db,
            reader=reader,
            uid=uid,
            badge=None,
            user=None,
            authorized=False,
            reason="reader_disabled",
        )

    badge = db.scalar(
        select(Badge).where(Badge.uid == uid)
    )

    if badge is None:
        return _record_result(
            db=db,
            reader=reader,
            uid=uid,
            badge=None,
            user=None,
            authorized=False,
            reason="unknown_badge",
        )

    user = db.get(User, badge.user_id)

    if not badge.active:
        return _record_result(
            db=db,
            reader=reader,
            uid=uid,
            badge=badge,
            user=user,
            authorized=False,
            reason="badge_disabled",
        )

    if user is None:
        return _record_result(
            db=db,
            reader=reader,
            uid=uid,
            badge=badge,
            user=None,
            authorized=False,
            reason="user_not_found",
        )

    if not user.active:
        return _record_result(
            db=db,
            reader=reader,
            uid=uid,
            badge=badge,
            user=user,
            authorized=False,
            reason="user_disabled",
        )

    return _record_result(
        db=db,
        reader=reader,
        uid=uid,
        badge=badge,
        user=user,
        authorized=True,
        reason="authorized",
    )


def _record_result(
    db: Session,
    reader: Reader,
    uid: str,
    badge: Badge | None,
    user: User | None,
    authorized: bool,
    reason: str,
) -> AccessCheckResponse:
    event = AccessEvent(
        uid=uid,
        reader_id=reader.id,
        badge_id=badge.id if badge else None,
        user_id=user.id if user else None,
        authorized=authorized,
        reason=reason,
    )

    db.add(event)
    db.commit()

    return AccessCheckResponse(
        authorized=authorized,
        reason=reason,
        uid=uid,
        user_id=user.id if user else None,
        user_name=user.full_name if user else None,
    )
