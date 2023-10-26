import grpc
import math
import os
import time
import backend_pb2_grpc
import backend_pb2
from google.protobuf.empty_pb2 import Empty
from google.protobuf.timestamp_pb2 import Timestamp


def now():
    t = Timestamp()
    t.GetCurrentTime()
    return t


def backend_stub():
    host = os.getenv("BACKEND_GRPC_HOST")
    return backend_pb2_grpc.PricingStub(
        grpc.insecure_channel(f'{host}:50051')
    )


def integrator(backend_stub):
    price = backend_stub.GetLatestPrice(Empty()).price
    backend_stub.SavePrice(
        backend_pb2.Stock(
            symbol="AAPL",
            price=50.0 * math.sin(price/100.0) + 100,
            timestamp=now()
        ),
    )


if __name__ == "__main__":
    stub = backend_stub()

    while True:
        integrator(stub)
        time.sleep(1)
