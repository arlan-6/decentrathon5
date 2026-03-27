from collections.abc import Iterator


class DummySession:
    """Placeholder session type for future DB integration."""


def get_db() -> Iterator[DummySession]:
    yield DummySession()

