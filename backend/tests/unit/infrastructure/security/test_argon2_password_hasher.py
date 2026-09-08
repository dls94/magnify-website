from infrastructure.security.argon2_password_hasher import Argon2PasswordHasher


def test_hash_returns_argon2_hash():
    hasher = Argon2PasswordHasher()

    password_hash = hasher.hash("correct-password")

    assert password_hash.startswith("$argon2")


def test_hash_does_not_return_plain_password():
    hasher = Argon2PasswordHasher()

    password_hash = hasher.hash("correct-password")

    assert password_hash != "correct-password"


def test_same_password_produces_different_hashes():
    hasher = Argon2PasswordHasher()

    first_hash = hasher.hash("correct-password")
    second_hash = hasher.hash("correct-password")

    assert first_hash != second_hash


def test_verify_returns_true_for_correct_password():
    hasher = Argon2PasswordHasher()

    password_hash = hasher.hash("correct-password")

    assert hasher.verify("correct-password", password_hash) is True


def test_verify_returns_false_for_incorrect_password():
    hasher = Argon2PasswordHasher()

    password_hash = hasher.hash("correct-password")

    assert hasher.verify("wrong-password", password_hash) is False


def test_verify_returns_false_for_invalid_hash():
    hasher = Argon2PasswordHasher()

    assert hasher.verify("correct-password", "not-a-valid-hash") is False