import re

_UID_SEPARATORS = re.compile(r"[\s:-]+")
_HEX_UID = re.compile(r"^[0-9A-F]+$")


def normalize_uid(uid: str) -> str:
    """Return an RFID UID as uppercase hexadecimal without separators."""
    normalized = _UID_SEPARATORS.sub("", uid.strip()).upper()

    if not normalized:
        raise ValueError("RFID UID cannot be empty")

    if not _HEX_UID.fullmatch(normalized):
        raise ValueError("RFID UID must contain only hexadecimal characters")

    if len(normalized) % 2 != 0:
        raise ValueError("RFID UID must contain complete hexadecimal bytes")

    if len(normalized) > 32:
        raise ValueError("RFID UID is too long")

    return normalized
