import pytest
import os
import grpc

import backend_pb2
import backend_pb2_grpc

from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.empty_pb2 import Empty

import service


@pytest.fixture
def backend_stub():
    host = os.getenv("BACKEND_GRPC_HOST") or "localhost"
    if host == "localhost":
        service.run()
    return backend_pb2_grpc.PricingStub(
        grpc.insecure_channel(f'{host}:50051')
    )


def now():
    t = Timestamp()
    t.GetCurrentTime()
    return t


def test_SavePrice(backend_stub):
    backend_stub.SavePrice(
        backend_pb2.Stock(
            symbol="AAPL",
            price=123.0,
            timestamp=now()
        ),
    )


def test_GetLatestPrice(backend_stub):
    price = backend_stub.GetLatestPrice(Empty())
    assert price.symbol == "AAPL"
