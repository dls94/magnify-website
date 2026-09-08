from application.ports.password_hasher import PasswordHasherPort


def test_password_hasher_port_defines_hash_and_verify():
    assert hasattr(PasswordHasherPort, "hash")
    assert hasattr(PasswordHasherPort, "verify")