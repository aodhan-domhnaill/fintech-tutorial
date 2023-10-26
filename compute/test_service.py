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


def test_integrator(backend_stub):
    service.integrator(backend_stub)
