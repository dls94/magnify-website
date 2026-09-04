from infrastructure.database.dependencies import get_session


async def test_get_session_provides_async_session():
    session_generator = get_session()

    session = await session_generator.__anext__()

    try:
        assert session is not None
    finally:
        await session_generator.aclose()