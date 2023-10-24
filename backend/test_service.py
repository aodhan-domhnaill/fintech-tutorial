import pytest
import os
import grpc

import backend_pb2
import backend_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
import service

@pytest.fixture
def service_stub():
    host = os.getenv("GRPC_HOST") or "localhost"
    if host == "localhost":
        service.run()
    return backend_pb2_grpc.PricingStub(
        grpc.insecure_channel(f'{host}:50051')
    )

def now():
    t = Timestamp()
    t.GetCurrentTime()
    return t

def test_SavePrice(service_stub):
    
    service_stub.SavePrice(
        backend_pb2.Stock(
            symbol="AAPL",
            price=123.0,
            timestamp=now()
        ),
    )
