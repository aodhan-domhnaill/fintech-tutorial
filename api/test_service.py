import pytest
import os
import service
from unittest.mock import MagicMock


@pytest.fixture
def backend_stub():
    host = os.getenv("BACKEND_GRPC_HOST") or "localhost"
    if host != "localhost":
        return service.backend_stub()
    else:
        stub = MagicMock()

        return stub


def test__add_price(backend_stub):
    service._add_price(123.0, backend_stub)
