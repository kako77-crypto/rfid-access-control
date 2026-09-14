from app.security import hash_api_key, verify_api_key


def test_hash_api_key_is_deterministic() -> None:
    api_key = "test-reader-secret"

    assert hash_api_key(api_key) == hash_api_key(api_key)


def test_verify_api_key_accepts_correct_key() -> None:
    api_key = "test-reader-secret"
    expected_hash = hash_api_key(api_key)

    assert verify_api_key(api_key, expected_hash) is True


def test_verify_api_key_rejects_wrong_key() -> None:
    expected_hash = hash_api_key("correct-secret")

    assert verify_api_key("wrong-secret", expected_hash) is False
