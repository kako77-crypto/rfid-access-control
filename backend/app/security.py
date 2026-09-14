import hashlib
import hmac


def hash_api_key(api_key: str) -> str:
    """Return the SHA-256 hexadecimal digest of an API key."""
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def verify_api_key(api_key: str, expected_hash: str) -> bool:
    """Verify an API key using a constant-time comparison."""
    candidate_hash = hash_api_key(api_key)

    return hmac.compare_digest(candidate_hash, expected_hash)
