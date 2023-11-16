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
        stub.GetMvgAvg.return_value.price = 888.88
        return stub


def test__add_price(backend_stub):
    p = service._add_price(123.0, backend_stub)
    assert p['price'] == 123.0


def test__get_mvg_avg(backend_stub):
    p = service._get_mvg_avg(backend_stub)
    assert p['price'] <= 888.88
