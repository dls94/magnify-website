from application.ports.token_provider import TokenProviderPort


def test_token_provider_port_defines_create_and_decode():
    assert hasattr(TokenProviderPort, "create_access_token")
    assert hasattr(TokenProviderPort, "decode_access_token")