import pytest
import os
import grpc
import datetime

import backend_pb2
import backend_pb2_grpc

from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.empty_pb2 import Empty

from unittest.mock import MagicMock

import service


@pytest.fixture
def backend_stub():
    host = os.getenv("BACKEND_GRPC_HOST") or "localhost"
    if host == "localhost":
        pgmock = MagicMock()
        curmock = pgmock.cursor.return_value.__enter__.return_value
        curmock.fetchone.return_value = (
            datetime.datetime.now(), 200.2, "AAPL")
        service.run(dbconn=pgmock)
    return backend_pb2_grpc.PricingStub(
        grpc.insecure_channel(f'{host}:50051')
    )


@pytest.fixture
def mvgavg_stub():
    host = os.getenv("BACKEND_GRPC_HOST") or "localhost"
    if host == "localhost":
        pgmock = MagicMock()
        curmock = pgmock.cursor.return_value.__enter__.return_value
        curmock.fetchone.return_value = (200.2, )
        service.run(dbconn=pgmock)
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


def test_GetMvgPrice(mvgavg_stub):
    price = mvgavg_stub.GetMvgAvg(Empty())
    assert price.price > 123
